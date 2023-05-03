import os, json, requests, sys, requests
from dotenv import load_dotenv
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored
from collections import deque
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils

## this function is not used anymo
def searchTitle(searchTpoic):
    messages = [
        {"role": "system", 
        "content": "You are a research assistant who will help me summarize the research topic and target outcomes I provide into 1 sentence.\
        Your summary should be a single query that I can put into google search. Reply me the result without including 'Research Query'."}
    ]
    searchQuery = utils.singleGPT(messages, searchTpoic)
    searchQuery = searchQuery.replace('"', '')
    print(colored("\nSearch Query Created:", 'blue',attrs=["bold", "underline"]), f" {searchQuery}")
    
    return searchQuery

## take the google search query and return the top 8 results URL
def google_official_search(query: str, num_results: int = 10) -> str | list[str]:
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

## take the url and look for information in the page
def searchContent(urls, SearchTopic, SearchObjectives, searchDomain, maxDepth, current_depth: int = 0, checkedURL=None, results=None):
    if checkedURL is None:
        checkedURL = set()
    if results is None:
        results = {
            'Related': pd.DataFrame(columns=['URL', 'Title', 'Content']),
            'Unrelated': pd.DataFrame(columns=['URL', 'Title', 'Content'])
            }
    queue = deque([(url, current_depth) for url in urls]) # create a queue to store the urls and its depth

    while queue:
        url, current_depth = queue.popleft() # pop the first url in the queue
        wrapped_url = utils.Url(url)
        if wrapped_url not in checkedURL: ## don't check the same url twice
            checkedURL.add(wrapped_url) # add the url to the checked list
            response = utils.fetch_url(url) # fetch the url
            if response is None: # if the response is none, then skip it
                continue
            elif (response.headers.get('content-type','').lower()) == 'application/pdf': # check if the content is pdf and download it
                utils.download_pdf(url)
            elif response.status_code == 200:  # if the response is 200, then extract the page content
                print(colored('\n\U0001F9D0 Reading the website for queried information: ', 'yellow', attrs=['bold']), url)
                content, links, page_Title = utils.getWebpageData(response, searchDomain,url) # get the page title,content, and links
                pageSummary = utils.PageResult(SearchObjectives, content) # get the page summary based on the search query
                
                if "4b76bd04151ea7384625746cecdb8ab293f261d4" not in pageSummary.lower():
                    results['Related'] = pd.concat([results['Related'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True) # add the filtered result to the dataframe
                    utils.updateExcel(SearchTopic, "Related", results['Related'])                
                else:
                    results['Unrelated'] = pd.concat([results['Unrelated'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True)
                    utils.updateExcel(SearchTopic, "Unrelated", results['Unrelated'])

                print("\u2714\uFE0F", colored(' Done! Results has been saved!','green',attrs=['bold']), ' Current Depth: ', current_depth)
                if current_depth < maxDepth:
                    print(colored('\U0001F9D0 Seaching for additonal relavent websites on this page...', 'yellow', attrs=['bold']))
                    relaventURLs = utils.relaventURL(SearchTopic, links) # Get the highly relevant links from the page and make them into asbolute URLs
                    if relaventURLs:
                        for next_url in relaventURLs:
                            queue.append((next_url, current_depth + 1)) # Enqueue the relevant URLs with an increased depth
                        print("\u2714\uFE0F", colored(' Additional relavent websites to search:', 'green', attrs=['bold']) ,f" {relaventURLs}", '\n')
                    else:
                        print("\u2714\uFE0F", colored(' No additional relavent webisites found on this page.\n', 'green', attrs=['bold']))
                        continue
                else:
                    print(colored('\u2714\uFE0F  Maximum depth reached. No additional websites from this page will be searched.\n', 'green', attrs=['bold']))
                    continue
            else: # if the response is not 200, then skip it. This line should never be reached since the fetch_url function will return None if the response is not 200
                print(f"Failed to fetch the page. Status code: {response.status_code}")
                continue
        else:
            print(colored('\U0001F9D0 URL already checked:', 'green', attrs=['bold']), f' {url}')
            print(colored('\u2714\uFE0F  Skip to the next website.\n', 'green', attrs=['bold']))
        
    return results