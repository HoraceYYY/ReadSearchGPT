from bs4 import BeautifulSoup
import os, requests, sys, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils
import openai
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, unquote_plus, urljoin
from termcolor import colored


def getContentPrompt(topic, objectives_inputs):
    content_prompt = "\n".join(f"{i+1}. {topic} {obj}" for i, obj in enumerate(objectives_inputs) if obj)
    return content_prompt

def getURLPrompt(topic, objectives_inputs):
    url_prompt = f'{topic}: ' + ", ".join([f"{obj}" for obj in objectives_inputs if obj])
    return url_prompt

topic = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")
print(colored("\nPlease list 3 outcomes your would like to achieve!", "blue",attrs=["bold", "underline"]))
objectives_inputs = [input(colored(f"Objective {i + 1}: ", "blue", attrs=["bold"])) for i in range(3)]

print(getContentPrompt(topic, objectives_inputs))
print(getURLPrompt(topic, objectives_inputs))
promptforURL = getURLPrompt(topic, objectives_inputs)

url = "https://www.swfinstitute.org/profiles/venture-capital-firm/north-america"
searchDomain = "none"

#print(promptObjectives)

headers = {
    'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'
}
#get header and body of the reponse
try:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
   

if (response.headers.get('content-type','').lower()) == 'application/pdf': # check if the content is pdf and download it
    utils.download_pdf(url)
elif response.status_code == 200:  # if the response is 200, then extract the page content
    content, links, page_Title = utils.getWebpageData(response, searchDomain,url) # get the page title,content, and links
    #pageSummary = utils.PageResult(promptObjectives, content) # get the page summary based on the search query
    #print(pageSummary)
    relaventURLs = utils.relaventURL(promptforURL, links)