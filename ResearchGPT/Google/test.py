from bs4 import BeautifulSoup
import os, requests, sys, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils, math
import openai
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, unquote_plus, urljoin
from termcolor import colored

# topic = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")
# objectives_input = [input(colored(f"Objective {i + 1}: ", "blue", attrs=["bold"])) for i in range(3)]
# non_empty_objectives = [f"{i + 1}. {obj}" for i, obj in enumerate(objectives_input) if obj]
# objectives = topic + "\n"+ "\n".join(non_empty_objectives)



url = 'https://appian.com/products/platform/overview.html'
headers = {
    'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'
}
try:
    response = requests.get(url, headers=headers)
    
except Exception as e:
    print(f"An error occurred: {e}")
     # if the url is not valid, then skip for the rest of the for loop


if (response.headers.get('content-type','').lower()) == 'application/pdf': # check if the content is pdf and download it
    utils.download_pdf(url)
elif response.status_code == 200:  # if the response is 200, then extract the page content
    page_content = response.text
    # extract the page content
    soup = BeautifulSoup(page_content, 'html.parser')
    for script in soup(['script', 'style']):# Remove any unwanted elements, such as scripts and styles, which may contain text that you don't want to extract
        script.decompose()
    text_content = soup.get_text(separator=' ') # Extract all the text content using the get_text() method
    clean_text = ' '.join(text_content.split()) # Clean up the extracted text by removing extra whitespace, line breaks, and other unnecessary characters
    # find all the links in the page
    links = []
    for a_tag in soup.find_all('a'):
        link = a_tag.get('href')
        if link:
            absolute_url = urljoin(url, link)
            links.append(absolute_url)
 # get result from the page; check question and contect of the page in gpt3.5 -> summary + url + webpage title
    relaventURLs = utils.relaventURL("Appian Intelligent Automation", links)
    print(relaventURLs)


    
