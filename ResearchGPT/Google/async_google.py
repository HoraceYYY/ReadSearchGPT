import os, json, sys, asyncio
from dotenv import load_dotenv
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored
from collections import deque
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import async_utils

## take the google search query and return the top 8 results URL
def google_official_search(query: str, searchtype: int) -> str | list[str]:
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

        if searchtype == 1: # this is quick search
            num_results = 3 # only return top 3 results from google; these are results with >10% click through rate
        elif searchtype == 2: # this is thorogh search
            num_results = 5 # return top 5 results from google; these are results with >5% click through rate
        elif searchtype == 3: # this is deep search
            num_results = 10 # return top 10 results from google; these are results with >1% click through rate
        # Send the search query and retrieve the results
        result = (
            service.cse()
            .list(q=query, cx=custom_search_engine_id, num=num_results)
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

async def url_consumer(task, task_id, consumer_queue, consumer_checked_list, content_prompt, topic, results, producer_done):
    file_name = None
    while not producer_done[0] or not consumer_queue.empty():
        if task['status'] == 'cancelled':
            break
        url, depth = await consumer_queue.get()
        wrapped_url = async_utils.Url(url)
        if wrapped_url not in consumer_checked_list:
            consumer_checked_list.add(wrapped_url)
            soup, content_type, status_code = await async_utils.fetch_url(url) # fetch the url
            if status_code == 200:
                if content_type.lower() == 'application/pdf': # check if the content is pdf and download it
                    await async_utils.download_pdf(url)
                elif status_code == 200:
                    print(colored('\n\U0001F9D0 Consumer: Reading the website for queried information: ', 'yellow', attrs=['bold']), url)
                    content, page_Title = await async_utils.getWebpageData(soup) # get the page title,content, and links
                    pageSummary = await async_utils.PageResult(content_prompt, content) # get the page summary based on the search query
                    
                    if "4b76bd04151ea7384625746cecdb8ab293f261d4" not in pageSummary.lower():
                        results['Related'] = pd.concat([results['Related'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True) # add the filtered result to the dataframe
                        await async_utils.updateExcel(task_id, topic, "Related", results['Related'])                
                    else:
                        results['Unrelated'] = pd.concat([results['Unrelated'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True)
                        await async_utils.updateExcel(task_id, topic, "Unrelated", results['Unrelated'])

                    print("\u2714\uFE0F", colored(' Consumer: Done! Results has been saved!','green',attrs=['bold']), ' Current Depth: ', depth)
            else:
                print("\U0001F6AB", colored(f' Consumer: Website did not respond. Error code: {status_code}.','red',attrs=['bold']), ' Current Depth: ', depth, ' URL:', url)
        else:
            print(colored('\u2714\uFE0F  Consumer:The content in this URL has already been checked:', 'green', attrs=['bold']), f' {url}')
            print(colored('\u2714\uFE0F  Consumer: Skip to the next website.\n', 'green', attrs=['bold']))


async def url_producer(task, producer_queue, consumer_queue, producer_checked_list, searchDomain, url_prompt, max_depth, producer_done):
    while not producer_queue.empty():
        if task['status'] == 'cancelled':
            break
        url, depth = await producer_queue.get()

        if depth < max_depth:
            wrapped_url = async_utils.Url(url)
            if wrapped_url not in producer_checked_list:
                producer_checked_list.add(wrapped_url)
                print(colored(f'\U0001F9D0 Producer: Seaching for additonal relavent websites on {url}', 'yellow', attrs=['bold']))
                soup, content_type, status_code = await async_utils.fetch_url(url) # fetch the url
                if status_code == 200: 
                    links = await async_utils.getWebpageLinks(soup, searchDomain, url)
                    relaventURLs = await async_utils.relaventURL(url_prompt, links) # Get the highly relevant links from the page and make them into asbolute URLs
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
    producer_done[0] = True  # Signal the consumer that the producer is done


async def main(task, task_id, topic, objectives_inputs, userDomain, max_depth):

    producer_queue = asyncio.Queue() #all urls here are raw / not wrapped
    consumer_queue = asyncio.Queue() #all urls here are raw / not wrapped

    content_prompt = async_utils.getContentPrompt(topic, objectives_inputs)
    url_prompt = async_utils.getURLPrompt(topic, objectives_inputs)
    
    search_results_links = []
    non_empty_objectives = [f"{topic} {obj}" for obj in objectives_inputs if obj]
    for objective in non_empty_objectives:
        if userDomain != None: # if the user wants to search within a domain. None if the user keep the UI field empty
            searchDomain = async_utils.get_domain(userDomain)
            objective = objective + " site:" + searchDomain
        search_results_links += google_official_search(objective, max_depth)

    for url in search_results_links:
        await producer_queue.put((url, 0))
        await consumer_queue.put((url, 0))

    producer_checked_list = set() #all urls here are wrapped
    consumer_checked_list = set() #all urls here are wrapped
    
    results = {
        'Related': pd.DataFrame(columns=['URL', 'Title', 'Content']),
        'Unrelated': pd.DataFrame(columns=['URL', 'Title', 'Content'])
        }
    
    producer_done = [False]

    num_producers = 1
    num_consumers = 1

    producer_tasks = [asyncio.create_task(url_producer(task, producer_queue, consumer_queue, producer_checked_list, searchDomain, url_prompt, max_depth, producer_done)) for _ in range(num_producers)]
    consumer_tasks = [asyncio.create_task(url_consumer(task, task_id, consumer_queue, consumer_checked_list, content_prompt, topic, results, producer_done)) for _ in range(num_consumers)]

    await asyncio.gather(*(producer_tasks + consumer_tasks))
    
    file_path = consumer_tasks[-1].result()[-1] 
 
    
    return file_path

""""
sudo code:

producer function(producer queue, consumer queue, producer checked list, max depth):
    
    while queue is not empty:
        pop the first url in the queue
        if the depth of the url < max depth:
            if the url is not in the producer checked list: 
                add the url to the producer checked list
                fetch relevant urls from the page
                add the relevant relevant urls to the producer queue
                add the relevant relevant urls to the consumer queue
            else:
                skip to the next url
    
    set flag for signal to consumer that producer is done

consumer function(consumer queue, consumer checked list):
    
    while producer is not done and consumer queue is not empty:
        pop the first url in the queue
        if the url is not in the consumer checked list:
            add the url to the consumer checked list
            fetch the url content and add to excel
        else:  
            skip to the next url

main function:       
    create a producer queue and initialize it with the urls from google. url should be wrapped before push
    create a consumer queue and initialize it with the urls from google. url should be wrapped before push
    create a empty producer checked list as a set
    create a empty consumer checked list as a set

    create a producer task
    create a consumer task
    gather the tasks

"""