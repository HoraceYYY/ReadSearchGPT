from bs4 import BeautifulSoup
import os, requests, sys, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils, math
import openai
from dotenv import load_dotenv

from termcolor import colored

objectives_input = [input(colored(f"Objective {i + 1}: ", "blue", attrs=["bold"])) for i in range(3)]
non_empty_objectives = [f"{i + 1}. {obj}" for i, obj in enumerate(objectives_input) if obj]
objectives = "\n".join(non_empty_objectives)

print("Objectives:")
print(objectives)


# def load_text_file(file_name):
#     with open(file_name, "r") as file:
#         return file.read()

# print(utils.num_tokens_from_string(load_text_file("Appian software overview/ modules and clientele_clean.txt")))


# url = 'https://www.tripadvisor.com/Attractions-g154943-Activities-Vancouver_British_Columbia.html'
# headers = {
#     'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'
# }
# try:
#     response = requests.get(url, headers=headers)
    
# except Exception as e:
#     print(f"An error occurred: {e}")
#      # if the url is not valid, then skip for the rest of the for loop


# if (response.headers.get('content-type','').lower()) == 'application/pdf': # check if the content is pdf and download it
#     utils.download_pdf(url)
# elif response.status_code == 200:  # if the response is 200, then extract the page content
#     page_content = response.text
#     # extract the page content
#     soup = BeautifulSoup(page_content, 'html.parser')
#     for script in soup(['script', 'style']):# Remove any unwanted elements, such as scripts and styles, which may contain text that you don't want to extract
#         script.decompose()
#     text_content = soup.get_text(separator=' ') # Extract all the text content using the get_text() method
#     clean_text = ' '.join(text_content.split()) # Clean up the extracted text by removing extra whitespace, line breaks, and other unnecessary characters
#     # find all the links in the page
    
#  # get result from the page; check question and contect of the page in gpt3.5 -> summary + url + webpage title
#     pageSummary = utils.PageResult("Appian modules functionality examples", clean_text)
#     title_tag = soup.find('title')
#     page_Title = title_tag.text if title_tag else None  # Return the title text if the title tag is found, otherwise return None
#     fullSummary = 'Website: '+ page_Title + '\n'+ 'url: '+ url + '\n' + 'Summary: '+ pageSummary + '\n'
#     links = []
#     for a_tag in soup.find_all('a'):
#         link = a_tag.get('href')
#         if link:
#             links.append(link)
    
#     relaventURLs = utils.relaventURL(url,"Appian system components and current customers", links)
#     print("\n\nfinal processed:", relaventURLs)
    
# Bold text
print(f"\033[1mThis text is bold!\033[0m")

# Underlined text
print(f"\033[4mThis text is underlined!\033[0m \n")

# Red text on a yellow background
print(f"\033[31m\033[43mRed text on a yellow background\033[0m")

# Define some ANSI escape codes for colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

# Use the escape codes to change the color of printed text
print(f"{RED}This text is red!{RESET}")
print(f"{GREEN}This text is green!{RESET}")
print(f"{YELLOW}This text is yellow!{RESET}")
print(f"{BLUE}This text is blue!{RESET}")
print(f"{MAGENTA}This text is magenta!{RESET}")
print(f"{CYAN}This text is cyan!{RESET}")
print(f"{WHITE}This text is white!{RESET}")
