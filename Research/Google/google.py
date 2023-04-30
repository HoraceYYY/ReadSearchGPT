import os, json, requests, sys, requests, openai
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils


## take the user input and covnert into a google search query
def searchTitle(searchTpoic):
    messages = [
        {"role": "system", 
        "content": "You are a research assistant who will help me generate a search query based on the research topic and target outcomes I provide. \
        Your summary should be a single search query that I can put into google search.\
        Only return me the search query without " " so that I can put in the google search."}
    ]
    searchQuery = utils.singleGPT(messages, searchTpoic)
    searchQuery = searchQuery.replace('"', '')
    print(colored("\nSearch Query Created:", 'blue',attrs=["bold", "underline"]), f" {searchQuery}")
    
    return searchQuery

## take the google search query and return the top 8 results URL
def google_official_search(query: str, num_results: int = 8) -> str | list[str]:
    """Return the results of a Google search using the official Google API

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        str: The results of the search.
    """
    try:
        print(colored("\n\U0001F9D0 Searching...", 'yellow',attrs=["bold"]))
        # Get the Google API key and Custom Search Engine ID from the config file
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
def searchContent(urls, searchQuery, maxDepth, depth: int = 0, checkedURL=None, results=None):
    if checkedURL is None:
        checkedURL = []
    if results is None:
        results = {
            'Related': pd.DataFrame(columns=['URL', 'Title', 'Content']),
            'Unrelated': pd.DataFrame(columns=['URL', 'Title', 'Content'])
        }
    if depth > maxDepth:
        return
    for url in urls:
        if utils.is_url_in_list(url,checkedURL) == False: ## don't check the same url twice
            checkedURL.append(url) # add the url to the checked list
            print(colored('\n\U0001F9D0 Reading the website for queried information: ', 'yellow', attrs=['bold']), url)
            headers = {
                'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'
            }
            #get header and body of the reponse
            try:
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    print(f"Failed to fetch the page. Status code: {response.status_code}")
                    continue
            except Exception as e:
                print(f"An error occurred: {e}")
                continue # if the url is not valid, then skip for the rest of the for loop

            if (response.headers.get('content-type','').lower()) == 'application/pdf': # check if the content is pdf and download it
                utils.download_pdf(url)
            elif response.status_code == 200:  # if the response is 200, then extract the page content
                content, links, page_Title = utils.getWebpageData(response) # get the page title,content, and links
                pageSummary = utils.PageResult(searchQuery, content) # get the page summary based on the search query
                #fullSummary = 'Website: '+ page_Title + '\n'+ 'url: '+ url + '\n' + 'Summary: '+ pageSummary + '\n'
                
                if "4b76bd04151ea7384625746cecdb8ab293f261d4" not in pageSummary.lower():
                    #utils.addToFile(fullSummary,f"{searchQuery}_related") ## add filtered result to the file
                    results['Related'] = pd.concat([results['Related'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True) # add the filtered result to the dataframe
                    utils.updateExcel(searchQuery, "Related", results['Related'])                
                else:
                    #utils.addToFile(fullSummary,f"{searchQuery}_unrelated") ## add all the raw results to the file
                    results['Unrelated'] = pd.concat([results['Unrelated'], pd.DataFrame([{'URL': url, 'Title': page_Title, 'Content': pageSummary}])], ignore_index=True)
                    utils.updateExcel(searchQuery, "Unrelated", results['Unrelated'])


                print("\u2714\uFE0F", colored(' Done! Results has been saved!','green',attrs=['bold']), ' Current Depth: ', depth)
                print(colored('\U0001F9D0 Seaching for additonal relavent website on this page...', 'yellow', attrs=['bold']))
                # Get the highly relevant links from the page and make them into asbolute URLs
                relaventURLs = utils.relaventURL(url,searchQuery, links)
                if relaventURLs == None:
                    print("\u2714\uFE0F", colored(' No additional relavent webisites found on this page.\n', 'green', attrs=['bold']))
                    continue
                else:
                    print("\u2714\uFE0F", colored(' Additional relavent websites to search:', 'green', attrs=['bold']) ,f" {relaventURLs}", '\n')
                    # recursively call the function to check the relavent links
                    searchContent(relaventURLs, searchQuery, maxDepth, depth + 1, checkedURL, results)
            else: # if the response is not 200, then exit
                print(f"Failed to fetch the page. Status code: {response.status_code}")
                exit()
        else:
            print('URL already checked: ', url, '\n\n')
            continue
    
    return results

            