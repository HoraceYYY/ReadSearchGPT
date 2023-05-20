import os, json, sys, asyncio
from dotenv import load_dotenv
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored
from database import SessionLocal
from crud import get_task
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import async_utils

## take the google search query and return the top 8 results URL
def google_official_search(query: str, searchWidth: int) -> str | list[str]:
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
            .list(q=query, cx=custom_search_engine_id, num=searchWidth)
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

async def url_consumer(task_id, consumer_queue, consumer_checked_list, content_prompt, results, producer_done, api_key):
    db = SessionLocal()
    try:
        while not producer_done[0] or not consumer_queue.empty():
            url, depth = await consumer_queue.get()
            wrapped_url = async_utils.Url(url)
            if wrapped_url not in consumer_checked_list:
                consumer_checked_list.add(wrapped_url)
                soup, content_type, status_code = await async_utils.fetch_url(url, results) # fetch the url
                if status_code == 200:
                    
                    if content_type.lower() == 'application/pdf': # check if the content is pdf and download it
                        await async_utils.add_to_db(db, task_id, category="Unchecked Material", pdfs=url) # add pdf link to database
                        results['Unchecked Material'] = pd.concat([results['Unchecked Material'], pd.DataFrame([{'PDFs': url}])], ignore_index=True) #remove after database works

                        print("\u2714\uFE0F", colored(' Consumer: Done! Results has been saved!','green',attrs=['bold']), ' Current Depth: ', depth)
                        continue # go to next while loop
                    
                    print(colored('\n\U0001F9D0 Consumer: Reading the website for queried information: ', 'yellow', attrs=['bold']), url)
                    content, page_Title = async_utils.getWebpageData(soup) # get the page title,content, and links
                    pageSummary = await async_utils.PageResult(api_key, content_prompt, content) # get the page summary based on the search query
                    if "4b76bd04151ea7384625746cecdb8ab293f261d4" not in pageSummary.lower():
                        await async_utils.add_to_db(db, task_id, category='Related', url = url, title=page_Title, content=pageSummary)
                        results['Related'] = pd.concat([results['Related'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True) # remove if database works
                    else:
                        await async_utils.add_to_db(db, task_id, category='Unrelated', url = url, title=page_Title, content=pageSummary)
                        results['Unrelated'] = pd.concat([results['Unrelated'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True) # remove if database works
                    print("\u2714\uFE0F", colored(' Consumer: Done! Results has been saved!','green',attrs=['bold']), ' Current Depth: ', depth)
                else:
                    await async_utils.add_to_db(db, task_id, category="Unchecked Material", additional_links=url) # add additional unchecked link to database
                    print("\U0001F6AB", colored(f' Consumer: Website did not respond. Error code: {status_code}.','red',attrs=['bold']), ' Current Depth: ', depth, ' URL:', url)
            else:
                print(colored('\u2714\uFE0F  Consumer:The content in this URL has already been checked:', 'green', attrs=['bold']), f' {url}')
                print(colored('\u2714\uFE0F  Consumer: Skip to the next website.\n', 'green', attrs=['bold']))
    except asyncio.CancelledError:
            print(colored('\u2714\uFE0F  Consumer: Task Cancelled!','red',attrs=['bold']))
            raise            
    finally:
        print(colored('\u2714\uFE0F  Consumer: Done!','green',attrs=['bold']))
        db.close()

async def url_producer(producer_queue, consumer_queue, producer_checked_list, searchDomain, url_prompt, max_depth, producer_done, api_key):
    try:
        while not producer_queue.empty():
            url, depth = await producer_queue.get()
            if depth < max_depth: ## change this to max_depth back later 
                wrapped_url = async_utils.Url(url)
                if wrapped_url not in producer_checked_list:
                    producer_checked_list.add(wrapped_url)
                    print(colored(f'\U0001F9D0 Producer: Seaching for additonal relavent websites on {url}', 'yellow', attrs=['bold']))
                    soup, content_type, status_code = await async_utils.fetch_url(url) # fetch the url
                    if status_code == 200:
                        if content_type.lower() == 'application/pdf': # check if the content is pdf, if so, skip to the next url
                            continue
                        links = async_utils.getWebpageLinks(soup, searchDomain, url)
                        #print(links)
                        relaventURLs = await async_utils.relaventURL(url_prompt, links, api_key) # Get the highly relevant links from the page and make them into asbolute URLs
                        if relaventURLs:  
                            print("\u2714\uFE0F", colored(' Producer: Additional relavent websites to search:', 'green', attrs=['bold']) ,f" {relaventURLs}", '\n')  
                            for new_url in relaventURLs:
                                await producer_queue.put((new_url, depth + 1))
                                await consumer_queue.put((new_url, depth + 1))
                        else:
                            print("\u2714\uFE0F", colored(f' Producer: No additional relavent webisites found on {url}.\n', 'green', attrs=['bold']))
                    else:
                        print("\U0001F6AB", colored(f' Producer: Website did not respond. Error code: {status_code}.','red',attrs=['bold']), ' Current Depth: ', depth, ' URL:', url , '\n')
                else:
                    print(colored('\u2714\uFE0F Producer: URLs on this page have already been checked:', 'green', attrs=['bold']), f' {url}')
                    print(colored('\u2714\uFE0F  Producer: Skip to the next website.\n', 'green', attrs=['bold']))
    except asyncio.CancelledError:
        print(colored('\u2714\uFE0F  Producer: Task Cancelled!','red',attrs=['bold']))
        raise
    finally:
        producer_done[0] = True  # Signal the consumer that the producer is done
        print(colored('\u2714\uFE0F  Producer: Done!','green',attrs=['bold']))

async def termination_watcher(task_id, tasks):
    db = SessionLocal()
    try:
        while True:
            await asyncio.sleep(30)  # Check every 30 seconds
            task = get_task(db, task_id)
            db.refresh(task)
            # print(colored(f"\n\nTask Status: {task.status}\n\n", 'blue', attrs=['bold']))
            if task.status == 'Cancelled':
                for task in tasks:
                    task.cancel()
    finally:
        db.close()  # Make sure to close the session when you're done

async def main(task_id, searchqueries, userDomain, max_depth, searchWidth, api_key):
    producer_queue = asyncio.Queue() #all urls here are raw / not wrapped
    consumer_queue = asyncio.Queue() #all urls here are raw / not wrapped
    
    if userDomain is not None and userDomain.strip() == "": # remove this once the ui logic is done
        userDomain = None

    content_prompt = async_utils.getContentPrompt(searchqueries)
    url_prompt = async_utils.getURLPrompt(searchqueries)

    search_results_links = []
    searchDomain = None
    for query in searchqueries:
        if userDomain != None: # if the user wants to search within a domain. None if the user keep the UI field empty
            searchDomain = async_utils.get_domain(userDomain)
            query = query + " site:" + searchDomain
        search_results_links += google_official_search(query, searchWidth)

    for url in search_results_links:
        await producer_queue.put((url, 0))
        await consumer_queue.put((url, 0))

    producer_checked_list = set() #all urls here are wrapped
    consumer_checked_list = set() #all urls here are wrapped
    
    results = {
        'Related': pd.DataFrame(columns=['URL', 'Title', 'Content']),
        'Unrelated': pd.DataFrame(columns=['URL', 'Title', 'Content']),
        'Unchecked Material': pd.DataFrame(columns=['PDFs', 'Additional Links']),
        }
    
    producer_done = [False]

    num_producers = 1
    num_consumers = 1

    producer_tasks = [asyncio.create_task(url_producer(producer_queue, consumer_queue, producer_checked_list, searchDomain, url_prompt, max_depth, producer_done, api_key)) for _ in range(num_producers)]
    consumer_tasks = [asyncio.create_task(url_consumer(task_id, consumer_queue, consumer_checked_list, content_prompt, results, producer_done, api_key)) for _ in range(num_consumers)]

    all_tasks = producer_tasks + consumer_tasks
    watcher_task = asyncio.create_task(termination_watcher(task_id, all_tasks))

    await asyncio.gather(*all_tasks, return_exceptions=True)
    watcher_task.cancel()


