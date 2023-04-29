import requests, os, re, time
import shutil
import openai
from dotenv import load_dotenv
from urllib.parse import urljoin
import ast
import tiktoken, math
from urllib.parse import urlparse, parse_qs, unquote
from bs4 import BeautifulSoup

def singleGPT(systemMessages, userMessage, temperature=1, top_p=1, model='gpt-3.5-turbo'):
    load_dotenv()
    openai.organization = os.getenv("OPENAI_ORG")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    systemMessages.append({"role": "user", "content":userMessage})
    success = False
    response = None
    while not success:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=systemMessages,
                temperature=temperature,
                top_p=top_p
            )
            success = True
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

    return response["choices"][0]["message"]["content"]

def download_pdf(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    ## create download folder
    folder_path = 'Download_files'
    os.makedirs(folder_path, exist_ok=True)
    ## set name and path fo the pdf
    file_name = os.path.basename(url)
    output_path = os.path.join(folder_path, file_name)
    with open(output_path, 'wb') as output_file:
        shutil.copyfileobj(response.raw, output_file)
    print(f'PDF downloaded and saved to {output_path}')

def convert_to_absolute(base_url, urls):
    absolute_urls = []
    for url in urls:
        absolute_url = urljoin(base_url, ''.join(url))
        absolute_urls.append(absolute_url)
    return absolute_urls

def urls_are_same(url1, url2):
    parsed_url1 = urlparse(url1)
    parsed_url2 = urlparse(url2)

    # Normalize the scheme (e.g., treat 'http' and 'https' as equivalent)
    scheme1 = parsed_url1.scheme.lower()
    scheme2 = parsed_url2.scheme.lower()

    if scheme1 in ('http', 'https'):
        scheme1 = 'http'
    if scheme2 in ('http', 'https'):
        scheme2 = 'http'

    # Compare the netloc (domain and port) after converting to lowercase and removing 'www.'
    domain1 = parsed_url1.netloc.lower().replace("www.", "")
    domain2 = parsed_url2.netloc.lower().replace("www.", "")

    # Compare the path, after removing any trailing slashes and decoding URL-encoded characters
    path1 = unquote(parsed_url1.path.rstrip("/"))
    path2 = unquote(parsed_url2.path.rstrip("/"))

    # Compare query parameters
    query_params1 = parse_qs(parsed_url1.query)
    query_params2 = parse_qs(parsed_url2.query)

    # Compare fragments
    fragment1 = unquote(parsed_url1.fragment)
    fragment2 = unquote(parsed_url2.fragment)

    return (scheme1 == scheme2 and domain1 == domain2 and path1 == path2 and
            query_params1 == query_params2 and fragment1 == fragment2)

def is_url_in_list(target_url, url_list):
    for url in url_list:
        if urls_are_same(target_url, url):
            return True
    return False

def relaventURL(url, searchQuery, links):
    try:
        messages = [
            {"role": "system", 
            "content": "you are a link checking ai. you are designed to check if the list of the links from the webpage of the current link is relevant to the question I ask.\
            I will gave you 2 pieces of information: Question, Links. Based on the question I give you, you will return me the links that is extremely relevant to the question as a python array only, otherwise,  return 'NONE'"}
        ]
        ## pass the list of message to GPT
        links = convert_to_absolute(url, links)
        token = num_tokens_from_string(' '.join(links))
        if token <= 3500:
            urlMessage = "Question: " + searchQuery + "\nLinks:" + ' '.join(links)
            relaventURLs = singleGPT(messages,urlMessage, temperature=0.0, top_p=1)
            pattern = r'\[.*?\]' ## regex to extract the list of urls from the string in case gpt returns extra text
            relaventURLs = re.search(pattern, relaventURLs)
            if relaventURLs:
                relaventURLs = ast.literal_eval(relaventURLs.group())
            else:
                return None
        else:
            relaventURLs = LinksBreakUp(url, searchQuery, links) # split the links into subarrays of 3000 tokens
            list_strings = re.findall(r'\[.*?\]', relaventURLs) # Extract all the strings that are enclosed in square brackets into a list
            if list_strings: 
                extracted_lists = [ast.literal_eval(list_string) for list_string in list_strings] # Convert the strings into lists
                relaventURLs = [item for sublist in extracted_lists for item in sublist] # Flatten the 2D list into a 1D list
            else:
                return None
        return relaventURLs   
    except Exception as e:
        print(f"An error occurred in LinksBreakUp: {e}")
        return None
    
def LinksBreakUp(url, searchQuery, links): # convert the list of links into a string and break it up into subarrays of 3000 tokens. It will break up some links but give better speed
    try:
        linksString = ' '.join(links)
        relaventURLs = ' '
        tokenNumber = num_tokens_from_string(linksString)
        sectionNumber = math.ceil(tokenNumber/3000)
        cutoffIndex = math.ceil(len(linksString)/sectionNumber)
        #print(links)
        for i in range(sectionNumber):
            start_index = i * cutoffIndex
            end_index = (i + 1) * cutoffIndex
            section = linksString[start_index:end_index]
            #print('sectionToken',num_tokens_from_string(section))
            messages = [
                {"role": "system", 
                "content": "you are a link checking ai. you are designed to check if the list of the links from the webpage of the current link is relevant to the question I ask.\
            I will gave you 2 pieces of information: Question, Links. Based on the question I give you, you will return me the links that is extremely relevant to the question as a python array only, otherwise,  return 'NONE'"}
        ]
            urlMessage = "Question: " + searchQuery + "\nLinks:" + section
            relaventURLs += singleGPT(messages,urlMessage, temperature=0.0, top_p=1)
            # print(relaventURLs)
            # print('\n')
        return relaventURLs # return a text string of the links with potentially some text from GPT3.5
    except Exception as e:
        print(f"An error occurred in LinksBreakUp: {e}")
        return None
    
def num_tokens_from_string(string: str, encoding_name = 'cl100k_base' ) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def createFile(content,name):
    file_name = f"{name}.txt"
    with open(file_name, 'w') as file:
        file.write(content)
        file.write("\n\n\n")

def addToFile(content, name):
    file_name = f"{name}.txt"
    with open(file_name, 'a') as file:
        file.write(content)
        file.write("\n")

#break up the content of long webpages into smaller chunks and pass each into GPT3.5 to avoid the token limit and return the summary of the whole webpage
def pageBreakUp(searchQuery, content): 
    pageSummary = ''
    sectionNum = math.ceil(num_tokens_from_string(content) // 3500) + 1 
    cutoffIndex = math.ceil(len(content) // sectionNum)
    for i in range(sectionNum): #split the content into multiple section and use a new GPT3.5 for each section to avoid the token limit
        section_messages = [
            {"role": "system", 
            "content": "You are a question and answer AI. You will answer the question I ask you based on the Content I give you."}
            ]
        start_index = i * cutoffIndex
        end_index = (i + 1) * cutoffIndex
        section = content[start_index:end_index]
        pageMessage = "Question: " + searchQuery + "\nContent:" + section
        pageSummary += singleGPT(section_messages,pageMessage)
    return pageSummary

def PageResult(searchQuery, content):
    messages = [
        {"role": "system", 
        "content": "You are a searching AI. You will search the Query from the Content I provide you.\
         If the content does not contain the queried information, reply'4b76bd04151ea7384625746cecdb8ab293f261d4' and do not summarize the content."}
        ]
    pageSummary = ''
    if num_tokens_from_string(content) <= 4000: #if the content is less than 4000 tokens, pass the whole content to GPT
        pageMessage = "Query: " + searchQuery + "\nContent:" + content
        pageSummary = singleGPT(messages,pageMessage)
    else: #split the webpage content into multiple section to avoid the token limit
        pageSummary = pageBreakUp(searchQuery, content) #split the webpage content into multiple section and return the summary of the whole webpage
        pageSummary = "Query: " + searchQuery + "\nContent:" + pageSummary 
        pageSummary = singleGPT(messages,pageSummary)
    
    return pageSummary

def searchType():
    valid_inputs = ["quick", "deep", "thorough"]

    while True:
        searchType = input("Enter search type: 'Quick', 'Thorough' or 'Deep' \nSearch Type: ").lower()
        if searchType in valid_inputs:
            break
        else:
            print("Invalid input! Please enter either 'Quick' or 'Deep'.")
    
    if searchType == "quick":
        return 1
    elif searchType == "deep":
        return 3
    elif searchType == "thorough":
        return 2

def getWebpageData(response):
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
            links.append(link)
    title_tag = soup.find('title')
    page_Title = title_tag.text if title_tag else None
    return clean_text, links, page_Title