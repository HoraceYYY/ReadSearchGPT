import requests, os, re, time, shutil, openai, ast, tiktoken, math, asyncio, aiofiles
from aiohttp import ClientSession
from termcolor import colored
from dotenv import load_dotenv 
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qsl, unquote_plus, urljoin, parse_qs, unquote

# see https://github.com/openai/openai-python for async api details
async def singleGPT(systemMessages, userMessage, temperature=1, top_p=1, model='gpt-3.5-turbo'):
    load_dotenv()
    openai.organization = os.getenv("OPENAI_ORG")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.aiosession.set(ClientSession())
    systemMessages.append({"role": "user", "content":userMessage})
    success = False
    response = None
    
    while not success:
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=systemMessages,
                temperature=temperature,
                top_p=top_p
            )
            success = True
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)

    return response["choices"][0]["message"]["content"]
      
async def fetch_url(url):
    headers = {
        'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'
    }
    
    async with ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response
                else:
                    print(f"Failed to fetch the page. Status code: {response.status}")
                    return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

async def download_pdf(url):
    headers = {'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            ## create download folder
            folder_path = 'Downloaded_files'
            os.makedirs(folder_path, exist_ok=True)
            ## set name and path for the pdf
            file_name = os.path.basename(url)
            output_path = os.path.join(folder_path, file_name)
            async with aiofiles.open(output_path, 'wb') as output_file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    await output_file.write(chunk)
            print(colored(f'PDF downloaded and saved to {output_path}', 'green', attrs=['bold']))

def download_pdf(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    ## create download folder
    folder_path = 'Downloaded_files'
    os.makedirs(folder_path, exist_ok=True)
    ## set name and path fo the pdf
    file_name = os.path.basename(url)
    output_path = os.path.join(folder_path, file_name)
    with open(output_path, 'wb') as output_file:
        shutil.copyfileobj(response.raw, output_file)
    print(colored(f'PDF downloaded and saved to {output_path}'), 'green', attrs=['bold'])

# this function is not used anymore because it is replaced by the class URL
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

# this function is not used anymore because it is replaced by the class URL
def is_url_in_list(target_url, url_list):
    for url in url_list:
        if urls_are_same(target_url, url):
            return True
    return False

async def relaventURL(SearchTopic, links):
    try:
        messages = [
            {"role": "system", 
            "content": "you are a link checking ai. you are designed to check if the list of the links from the webpage of the current link is relevant to the question I ask.\
            I will gave you 2 pieces of information: Question, Links. Based on the question I give you, you will return me the links that is extremely relevant to the question as a python array only, otherwise,  return 'NONE'"}
        ]
        ## pass the list of message to GPT
        linksString = ' '.join(links)
        token = num_tokens_from_string(linksString)
        pattern = re.compile(r'\[.*?\]')
        if token <= 3500:
            urlMessage = "Question: " + SearchTopic + "\nLinks:" + ' '.join(links)
            relaventURLs = await singleGPT(messages,urlMessage, temperature=0.0, top_p=1)
            relaventURLs = re.search(pattern, relaventURLs)
            if relaventURLs:
                relaventURLs = ast.literal_eval(relaventURLs.group())
            else:
                return None
        else:
            relaventURLs = await LinksBreakUp(token, SearchTopic, linksString) # split the links into subarrays of 3000 tokens
            list_strings = re.findall(pattern, relaventURLs) # Extract all the strings that are enclosed in square brackets into a list
            if list_strings: 
                extracted_lists = [ast.literal_eval(list_string) for list_string in list_strings] # Convert the strings into lists
                relaventURLs = [item for sublist in extracted_lists for item in sublist] # Flatten the 2D list into a 1D list
            else:
                return None
        return relaventURLs   
    except Exception as e:
        print(f"An error occurred in LinksBreakUp: {e}")
        return None
    
async def LinksBreakUp(token, SearchTopic, linksString): # convert the list of links into a string and break it up into subarrays of 3000 tokens. It will break up some links but give better speed
    try:
        relaventURLs = ' '
        sectionNumber = math.ceil(token/3000)
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
            urlMessage = "Question: " + SearchTopic + "\nLinks:" + section
            relaventURLs += await singleGPT(messages,urlMessage, temperature=0.0, top_p=1)
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

def truncate_text_tokens(text, encoding_name='cl100k_base', max_tokens=3500):
    """Truncate a string to have `max_tokens` according to the given encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    return encoding.encode(text)[:max_tokens]

# this function is not used anymore because output is not text
def createFile(content,name):
    file_name = f"{name}.txt"
    with open(file_name, 'w') as file:
        file.write(content)
        file.write("\n\n\n")

# this function is not used anymore because output is not text
def addToFile(content, name):
    file_name = f"{name}.txt"
    with open(file_name, 'a') as file:
        file.write(content)
        file.write("\n")

#break up the content of long webpages into smaller chunks and pass each into GPT3.5 to avoid the token limit and return the summary of the whole webpage
async def pageBreakUp(SearchObjectives, content): 
    pageSummary = ''
    sectionNum = math.ceil(num_tokens_from_string(content) // 3000) + 1 
    cutoffIndex = math.ceil(len(content) // sectionNum)
    for i in range(sectionNum): #split the content into multiple section and use a new GPT3.5 for each section to avoid the token limit
        section_messages = [
            {"role": "system", 
            "content": "You are a searching AI. You will search the Query from the Content I provide you.\
            If the content does not contain the queried information, reply'4b76bd04151ea7384625746cecdb8ab293f261d4' and do not summarize the content."}
            ]
        start_index = i * cutoffIndex
        end_index = (i + 1) * cutoffIndex
        section = content[start_index:end_index]
        pageMessage = "Query: " + SearchObjectives + "\nContent:" + section
        pageSummary += await singleGPT(section_messages,pageMessage)
    if num_tokens_from_string(pageSummary) > 3500: #if the summary is still too long, truncate it to 3500 tokens
        pageSummary = truncate_text_tokens(pageSummary)
    return pageSummary

async def PageResult(SearchObjectives, content):
    messages = [
        {"role": "system", 
        "content": "You are a searching AI. You will search the Query from the Content I provide you.\
         If the content does not contain the queried information, reply'4b76bd04151ea7384625746cecdb8ab293f261d4' and do not summarize the content."}
        ]
    pageSummary = ''
    if num_tokens_from_string(content) <= 3500: #if the content is less than 3500 tokens, pass the whole content to GPT
        pageMessage = "Query: " + SearchObjectives + "\nContent:" + content
        pageSummary = await singleGPT(messages,pageMessage)
    else: #split the webpage content into multiple section to avoid the token limit
        pageSummary = await pageBreakUp(SearchObjectives, content) #split the webpage content into multiple section and return the summary of the whole webpage
        #print("pageSummary: ",pageSummary)
        pageSummary = "Query: " + SearchObjectives + "\nContent:" + pageSummary 
        pageSummary = await singleGPT(messages,pageSummary)

    return pageSummary

def searchType():
    valid_inputs = ["quick", "deep", "thorough"]

    while True:
        searchType = input(colored("\nEnter search type (Quick, Thorough, Deep):", "blue", attrs=["bold","underline"])+ " ").lower()
        if searchType in valid_inputs:
            break
        else:
            print("Invalid input! Please enter one of following: 'Quick', 'Thorough', 'Deep'.")
    
    if searchType == "quick":
        return 1
    elif searchType == "deep":
        return 3
    elif searchType == "thorough":
        return 2

def parseHTML(response):
    page_content = response.text
    # extract the page content
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup

def getWebpageData(response):
    soup = parseHTML(response)
    for script in soup(['script', 'style']):# Remove any unwanted elements, such as scripts and styles, which may contain text that you don't want to extract
        script.decompose()
    text_content = soup.get_text(separator=' ') # Extract all the text content using the get_text() method
    clean_text = ' '.join(text_content.split()) # Clean up the extracted text by removing extra whitespace, line breaks, and other unnecessary characters
    # find all the links in the page
    title_tag = soup.find('title')
    page_Title = title_tag.text if title_tag else None
    return clean_text, page_Title

def getWebpageLinks(response, searchDomain, url):
    soup = parseHTML(response)
    links = []
    for a_tag in soup.find_all('a'):
        link = a_tag.get('href')
        if link:
            absolute_url = urljoin(url, link)
            if searchDomain == 'none':
                links.append(absolute_url)
            elif searchDomain != 'none' and Url(absolute_url).is_from_domain(searchDomain):
                links.append(absolute_url)
    return links

async def updateExcel(excel_name, excelsheet, data):
    folder_path = 'Results'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    file_name = f"{folder_path}/{excel_name}.xlsx"  # Create the Excel file name
    if os.path.isfile(file_name):  # Check if the file exists
        xls = await asyncio.to_thread(pd.ExcelFile, file_name)  # If the file exists, read the existing Excel file
        if excelsheet in xls.sheet_names:  # Check if the sheet exists in the Excel file
            sheet_data = {}  # Create a dictionary to store all the sheets because they will be overwritten
            for sheet in xls.sheet_names:  # Read all the sheets and store them in the dictionary
                if sheet == excelsheet:
                    sheet_data[sheet] = data.copy()  # Overwrite the specified sheet with the updated data
                else:
                    sheet_df = await asyncio.to_thread(pd.read_excel, xls, sheet_name=sheet)
                    sheet_data[sheet] = sheet_df  # Store the data of the other sheets

            writer = await asyncio.to_thread(pd.ExcelWriter, file_name)  # Write all the sheets to the Excel file
            for sheet, df in sheet_data.items():
                await asyncio.to_thread(df.to_excel, writer, sheet_name=sheet, index=False)
            await asyncio.to_thread(writer.save)
        else:  # If the sheet doesn't exist, write the new data as a new sheet
            writer = await asyncio.to_thread(pd.ExcelWriter, file_name, mode='a')
            await asyncio.to_thread(data.to_excel, writer, sheet_name=excelsheet, index=False)
            await asyncio.to_thread(writer.save)
    else:  # If the file doesn't exist, write the new data as a new sheet
        await asyncio.to_thread(data.to_excel, file_name, sheet_name=excelsheet, index=False)
    return

def get_domain(url):
    parts = urlparse(url)
    return parts.netloc

class Url(object):
    '''A url object that can be compared with other url orbjects
    without regard to the vagaries of encoding, escaping, and ordering
    of parameters in query strings.'''

    def __init__(self, url):
        parts = urlparse(url)
        _query = frozenset(parse_qsl(parts.query))
        _path = unquote_plus(parts.path)
        parts = parts._replace(query=_query, path=_path)
        self.parts = parts

    def __eq__(self, other):
        return self.parts == other.parts

    def __hash__(self):
        return hash(self.parts)
    
    def is_from_domain(self, domain):
        return self.parts.netloc == domain
    
    