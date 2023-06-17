import os, json, sys, asyncio
from dotenv import load_dotenv
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored
from database import SessionLocal
import crud, models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import async_utils

## take the google search query and return the top 8 results URL
def google_official_search(query: str) -> str | list[str]:
    """Return the results of a Google search using the official Google API

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        str: The results of the search.
    """
    try:
        print(colored("\nSearch Query Created:", 'blue',attrs=["bold", "underline"]), f" {query}")
        print(colored("\n\U0001F9D0 Searching...", 'yellow',attrs=["bold"]))
        # Get the Google API key and Custom Search Engine ID from the config file
        load_dotenv()  # Load the .env file
        api_key = os.getenv("GOOGLE_API_KEY")
        custom_search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

        # Initialize the Custom Search API service
        service = build("customsearch", "v1", developerKey=api_key)

        # Send the search query and retrieve the results
        result = (
            service.cse()
            .list(q=query, cx=custom_search_engine_id, num=10)
            .execute()
        )

        # Extract the search result items from the response
        search_results = result.get("items", [])

        # Create a list of only the URLs from the search results
        search_results_links = [item["link"] for item in search_results]

    except HttpError as e:
        # Handle errors in the API call
        error_details = json.loads(e.content.decode())

        # Check if the error is related to an invalid or missing API key
        if error_details.get("error", {}).get(
            "code"
        ) == 403 and "invalid API key" in error_details.get("error", {}).get(
            "message", ""
        ):
            return "Error: The provided Google API key is invalid or missing."
        else:
            return f"Error: {e}"
    # google_result can be a list or a string depending on the search results

    # Return the list of search result URLs
    print("\n \u2714\uFE0F ", colored('Found following websites to search:', 'green',attrs=["bold", "underline"]))
    for link in search_results_links:
        print(link)
    #print(colored('\nSearching...', 'blue',attrs=["bold"]))
    return search_results_links
    #return safe_google_results(search_results_links)

async def url_consumer(db, url, query, queryid, api_key):
    try:
        soup, content_type, status_code = await async_utils.fetch_url(url) # fetch the url
        if status_code == 200:
            if content_type.lower() == 'application/pdf': # check if the content is pdf and download it
                await async_utils.add_to_URLData_db(db, queryid, category="PDFs", url=url) # add pdf link to database
                print("\u2714\uFE0F", colored(' Consumer: Done! PDF link has been saved!','green',attrs=['bold']))
                return
            print(colored('\n\U0001F9D0 Consumer: Reading the website for queried information: ', 'yellow', attrs=['bold']), url)
            content, page_Title = async_utils.getWebpageData(soup) # get the page title,content, and links
            pageSummary = await async_utils.PageResult(api_key, query, content) # get the page summary based on the search query
            await async_utils.add_to_URLData_db(db, queryid, category='Website_Content', url = url, title=page_Title, content=pageSummary)                      
            print("\u2714\uFE0F", colored(' Consumer: Done! Results has been saved!','green',attrs=['bold']))
        else:
            await async_utils.add_to_URLData_db(db, queryid, category="Unread_Websites", url=url) # add additional unchecked link to database
            print("\U0001F6AB", colored(f' Consumer: Website did not respond. Error code: {status_code}.','red',attrs=['bold']), ' URL:', url)
    except asyncio.CancelledError:
            print(colored('\u2714\uFE0F  Consumer: Task Cancelled!','red',attrs=['bold']))
            raise            

async def url_producer(db, searchDomain, url, query, queryid, api_key):
    try:       
        print(colored(f'\U0001F9D0 Producer: Seaching for additonal relavent websites on {url}', 'yellow', attrs=['bold']))
        soup, content_type, status_code = await async_utils.fetch_url(url) # fetch the url
        if status_code == 200:
            if content_type.lower() != 'application/pdf': # check if the content is pdf, if so, skip to the next url

                links = async_utils.getWebpageLinks(soup, searchDomain, url) # these links are defragmented and deduplcated and coverted to abs urls
                #print(links)
                relaventURLs = await async_utils.relaventURL(query, links, api_key) # Get the highly relevant links from the page links
                if relaventURLs:
                    await async_utils.add_to_URL_db(db, queryid, links, relaventURLs)  
                    print("\u2714\uFE0F", colored(' Producer: Additional relavent websites to search:', 'green', attrs=['bold']) ,f" {relaventURLs}", '\n')  
                else:
                    print("\u2714\uFE0F", colored(f' Producer: No additional relavent webisites found on {url}.\n', 'green', attrs=['bold']))
                return relaventURLs
        else:
            print("\U0001F6AB", colored(f' Producer: Website did not respond. Error code: {status_code}.','red',attrs=['bold']), ' URL:', url , '\n')
    except asyncio.CancelledError:
        print(colored('\u2714\uFE0F  Producer: Task Cancelled!','red',attrs=['bold']))
        raise

async def first_search(db, searchqueries, userDomain, api_key):
    if userDomain is not None and userDomain.strip() == "":
        userDomain = None
    searchDomain = None    
    search_results = {}  # Initialize an empty dictionary
    for query in searchqueries:
        if userDomain is not None:  # If the user wants to search within a domain
            searchDomain = async_utils.get_domain(userDomain)
            querywithsites = query + " site:" + searchDomain
            search_results[query] = google_official_search(querywithsites) ##  Save the search results associated with each query
        else:
            search_results[query] = google_official_search(query)

    research = crud.create_research(db) 
    
    all_tasks = []
    queryids = []
    for query in searchqueries:
        #create task database entry and query db entry
        query_row = models.Query(task_id = research.id, query = query)
        db.add(query_row)
        db.commit() # this will populate query_row.id
        queryids.append(query_row.id)
        url_row = models.URL(query_id = query_row.id, source = ["search_engine"], result = search_results[query])
        db.add(url_row)
        db.commit() # this will populate url.id
        ## consumer tasks run in parallel
        for url in search_results[query][:(len(search_results[query]) // 2)]: # Slice list to first half
            ##queryid = query_row.id
            task = asyncio.create_task(url_consumer(db, url, query, query_row.id, api_key)) ## this should save both results and raw urls in the table
            all_tasks.append(task)
    await asyncio.gather(*all_tasks) ## make sure all searches are done
    
    pageResults = {}  # List to store results from url_consumer
    for index, queryid in enumerate(queryids):
        url_data_objects = db.query(models.URLData.url, models.URLData.title, models.URLData.content).filter(models.URLData.query_id == queryid).all()
        pageResults[queryid] = [{"url": obj[0], "title": obj[1], "content": obj[2]} for obj in url_data_objects]
        contents = [obj[2] for obj in url_data_objects if obj[2] is not None]  # Extract non-null contents
        concatenated_content = " ".join(contents)  # Concatenate all contents with a space in between
        clean_content = ' '.join(concatenated_content.split())  # Remove all extra spaces
        # print(concatenated_content)
        querysummary = await async_utils.query_summary(api_key,searchqueries[index],clean_content)
        queru_summary_db = models.URLSummary(query_id = queryid, summarytype = "first_search", summary = querysummary)
        db.add(queru_summary_db)
        db.commit() 
        pageResults[queryid].append({"Summary": querysummary})
    queryresults = dict(zip(queryids, zip(searchqueries,pageResults.values())))
    return research.id, queryresults

async def second_search(db, queryid, api_key):
    all_tasks = []
    query_object= db.query(models.Query.query).filter(models.Query.id == queryid).first()
    urls_object = db.query(models.URL.result).filter(models.URL.query_id == queryid).first()
    query =query_object.query
    urls = urls_object.result
    for url in urls[(len(urls)//2) :]:
        ##print(url)
        task = asyncio.create_task(url_consumer(db, url, query, queryid, api_key))
        all_tasks.append(task)
    await asyncio.gather(*all_tasks) ## make sure all searches are done

    url_data_objects = db.query(models.URLData.url, models.URLData.title, models.URLData.content).filter(models.URLData.query_id == queryid).all()
    results = [{"url": obj[0], "title": obj[1], "content": obj[2]} for obj in url_data_objects]
    # print(results)
    contents = [obj[2] for obj in url_data_objects if obj[2] is not None]  # Extract non-null contents
    concatenated_content = " ".join(contents)  # Concatenate all contents with a space in between
    concatenated_content = ' '.join(concatenated_content.split())  # Remove all extra spaces
    print(concatenated_content)
    querysummary = await async_utils.query_summary(api_key,query,concatenated_content)
    queru_summary_db = models.URLSummary(query_id = queryid, summarytype = "second_search", summary = querysummary)
    db.add(queru_summary_db)
    db.commit() 
    results.append({"Summary": querysummary})
    queryresults = {queryid: [query, results]}
    return queryresults

async def first_deep_search(db, queryid, userDomain, api_key):
    searchDomain = None
    if userDomain is not None:
        if userDomain.strip() == "":
            userDomain = None
        else:
            searchDomain = async_utils.get_domain(userDomain)

    all_producer_tasks = []
    query_object= db.query(models.Query.query).filter(models.Query.id == queryid).first() # get query id
    urls_object = db.query(models.URL.result).filter(models.URL.query_id == queryid).first() #get query
    query =query_object.query
    urls = urls_object.result
    for url in urls[:(len(urls)//2)]: # only check first part of google urls to get new links
        task = asyncio.create_task(url_producer(db, searchDomain, url, query, queryid, api_key))
        all_producer_tasks.append(task)
    results = await asyncio.gather(*all_producer_tasks)  # this will contain all the relevantURLs from each task
    flat_results_set = set(item for sublist in results for item in sublist)
    urls_set = set(urls) # Convert urls to set
    relevantURLs = flat_results_set - urls_set # Subtract urls_set from flat_results_set to get only the new, unique URLs

    all_consumer_tasks = []
    for url in relevantURLs:
        task = asyncio.create_task(url_consumer(db, url, query, queryid, api_key))
        all_consumer_tasks.append(task)
    await asyncio.gather(*all_consumer_tasks)

    url_data_objects = db.query(models.URLData.url, models.URLData.title, models.URLData.content).filter(models.URLData.query_id == queryid).all()
    results = [{"url": obj[0], "title": obj[1], "content": obj[2]} for obj in url_data_objects]
    #print(results)
    contents = [obj[2] for obj in url_data_objects if obj[2] is not None]  # Extract non-null contents
    concatenated_content = " ".join(contents)  # Concatenate all contents with a space in between
    concatenated_content = ' '.join(concatenated_content.split())  # Remove all extra spaces
    print(concatenated_content)
    querysummary = await async_utils.query_summary(api_key,query,concatenated_content)
    queru_summary_db = models.URLSummary(query_id = queryid, summarytype = "first_deep_search", summary = querysummary)
    db.add(queru_summary_db)
    db.commit() 
    results.append({"Summary": querysummary})
    queryresults = {queryid: [query, results]}
    return queryresults