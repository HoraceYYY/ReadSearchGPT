from bs4 import BeautifulSoup
import os, requests, sys, json, asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import async_utils, utils
import openai
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, unquote_plus, urljoin
from termcolor import colored
import tracemalloc
tracemalloc.start()

def getContentPrompt(query_list):
    content_prompt = "\n".join(f"{i+1}. {obj}" for i, obj in enumerate(query_list))
    return content_prompt

def getURLPrompt(query_list):
    url_prompt = ", ".join([f"{obj}" for obj in query_list])
    return url_prompt

def creatSearchQuery(userAsk):
    messages = [
                {"role": "system", 
                 "content": "Generate up to 4 Google search queries using the following text. \
For each query, utilize specific keywords that accurately represent the topic. \
Ensure all queries are mutually exclusive and collectively exhaustive regarding the text's search content. \
Provide the search queries as a comma-separated list, without additional text. Example result format: 'https://www.example.com, https://www.example.com, https://www.example.com'"}]
    
    queryMessage = "Text:\n" + userAsk
    googleQueries = utils.singleGPT(messages, queryMessage, temperature=0.0, top_p=1)
    query_list = [query.strip() for query in googleQueries.split(',')] # remove the white space from the string and convert the string into a list
    return query_list


# userAsk = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")

# query_list = creatSearchQuery(userAsk)
# print(query_list)


# print(getContentPrompt(query_list))
# print(getURLPrompt(query_list))



async def run_task(url, content_prompt):
    soup, content_type, status_code = await async_utils.fetch_url(url) # fetch the url
    if status_code == 200:
        if content_type.lower() == 'application/pdf': # check if the content is pdf and download it
            await async_utils.download_pdf(url)
        else:
            print(colored('\n\U0001F9D0 Consumer: Reading the website for queried information: ', 'yellow', attrs=['bold']), url)
            content, page_Title = async_utils.getWebpageData(soup) # get the page title,content, and links
            pageSummary = await async_utils.PageResult(content_prompt, content) # get the page summary based on the search query
    print(f'{pageSummary}')
    return pageSummary

url = "https://en.wikipedia.org/wiki/Prince_George,_British_Columbia"
searchDomain = "none"
content_prompt = "1. school and university location and phone number in alberta Dawson Creek \n2. school and university location and phone number in alberta Fort St John\n3. school and university location and phone number in alberta Prince George "


asyncio.run(run_task(url, content_prompt))

tracemalloc.stop()