from bs4 import BeautifulSoup
import os, requests, sys, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils, math
import openai
from dotenv import load_dotenv

def load_text_file(file_name):
    with open(file_name, "r") as file:
        return file.read()

# print(utils.num_tokens_from_string(load_text_file("Appian software overview/ modules and clientele_clean.txt")))


url = 'https://www.tripadvisor.com/Attractions-g154943-Activities-Vancouver_British_Columbia.html'
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
    
 # get result from the page; check question and contect of the page in gpt3.5 -> summary + url + webpage title
    pageSummary = utils.PageResult("Appian modules functionality examples", clean_text)
    title_tag = soup.find('title')
    page_Title = title_tag.text if title_tag else None  # Return the title text if the title tag is found, otherwise return None
    fullSummary = 'Website: '+ page_Title + '\n'+ 'url: '+ url + '\n' + 'Summary: '+ pageSummary + '\n'
    links = []
    for a_tag in soup.find_all('a'):
        link = a_tag.get('href')
        if link:
            links.append(link)
    
    relaventURLs = utils.relaventURL(url,"Appian system components and current customers", links)
    print("\n\nfinal processed:", relaventURLs)
    
