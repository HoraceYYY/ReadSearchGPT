import os,  openai, tiktoken, math, asyncio, aiofiles, aiohttp
from termcolor import colored
##from dotenv import load_dotenv 
from bs4 import BeautifulSoup
import pandas as pd
import models
from urllib.parse import urlparse, parse_qsl, unquote_plus, urljoin, urldefrag

# see https://github.com/openai/openai-python for async api details
async def singleGPT(api_key, systemMessages, userMessage, temperature=1, top_p=1, model='gpt-3.5-turbo'):
    ##load_dotenv()
    ##openai.organization = os.getenv("OPENAI_ORG")
    openai.api_key = api_key
    openai.aiosession.set(aiohttp.ClientSession())
    systemMessages.append({"role": "user", "content":userMessage})
    max_retries = 3
    response = None

    for attempt in range(1, max_retries + 1):
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=systemMessages,
                temperature=temperature,
                top_p=top_p
            )
            break  # If successful, break out of the loop
        except Exception as e:
            if attempt < max_retries:
                print(f"An error occurred: {str(e)}")
                print(f"Retrying in 5 seconds... (attempt {attempt} of {max_retries})")
                await asyncio.sleep(5)
            else:
                print(f"An error occurred: {str(e)}")
                print(f"Reached the maximum number of retries ({max_retries}). Aborting.")
                await openai.aiosession.get().close()
                return str(e)  # You can return None or an appropriate default value here
    # Close the aiohttp session at the end
    await openai.aiosession.get().close()
    return response["choices"][0]["message"]["content"]
      
async def fetch_url(url, results = None):
    headers = {
        'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'
    }
    timeout = aiohttp.ClientTimeout(total=10)
    session = aiohttp.ClientSession(timeout=timeout)
    try:
        async with session.get(url, headers=headers) as response:
            content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
            status_code = response.status

            if status_code == 200:
                if content_type.lower() == 'application/pdf':
                    return None, content_type, status_code

                page_content = await response.text()
                # extract the page content
                soup = BeautifulSoup(page_content, 'html.parser')
                return soup, content_type, status_code
            else:
                print(f"Failed to fetch the page. Status code: {status_code}")
                results['Unchecked Material'] = pd.concat([results['Unchecked Material'], pd.DataFrame([{'Additional Links': url}])], ignore_index=True) # remove if database works
                return None, None, status_code
    except Exception as e:
        print(f"An error occurred. ERROR TYPE: {type(e)}; ERROR: {str(e)}")
        results['Unchecked Material'] = pd.concat([results['Unchecked Material'], pd.DataFrame([{'Additional Links': url}])], ignore_index=True) # remove if database works
        return None, None, None
    finally:
        await session.close()

async def add_to_db(session, task_id, category, url=None, title=None, content=None,  pdfs = None, additional_links=None):
    try:
        new_data = models.URLData(
            task_id=task_id,
            url=url,
            title=title,
            content=content,
            pdfs=pdfs,
            additional_links=additional_links,
            category=category
        )
        session.add(new_data)
        session.commit()
    except Exception as e:
        print(f"An error occurred while adding data to the database: {e}")
        session.rollback()

async def download_pdf(url): # not being used
    headers = {'User-Agent': 'Chrome/89.0.4389.82 Safari/537.36'}
    async with aiohttp.ClientSession() as session:
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

async def relaventURL(url_prompt, links, api_key):
    try:
        linksString = ','.join(links)
        #print(linksString)
        messages = [
            {"role": "system", 
            "content": f"From the URLs below, delimted by three dashes(-), extract the URLs that are most relevant to the target information I provide. \
If there are no URLs that are relevant to the target information, refrain from returning any messages. Instead of returning any messages, only return 'NONE'. \
Otherwise, return no more than 10 URLs unless there are additional URLs that are still extremely relevant to the target information. Refrain from returning more than 15 URLs in total. \
The order of relevance is important. The first URL should be the most relevant. \
Refrain from generating any additional text associated with the URLs. Only return the URL in comma_seperated_list_of_url, for example: url1,url2,url3. Refrain from using any other format for the output.\
Refrain from returning any URL that is not relevant to the target information. If you are not sure if the URL is relevant, refrain from returning the URL.\n\n\
---\n{linksString}\n---"}]
        ## pass the list of message to GPT

        token = num_tokens_from_string(linksString)
        if token <= 3500:
            urlMessage = "Target Information:" + url_prompt
            relaventURLs = await singleGPT(api_key, messages,urlMessage, temperature=0.0, top_p=1)
        else:
            relaventURLs = await LinksBreakUp(api_key, token, url_prompt, linksString) # split the links into subarrays of 3000 tokens
        
        if relaventURLs:
            relaventURLs = [url.strip() for url in relaventURLs.split(',')] # remove the white space from the string and convert the string into a list
            filtered_url_list = [url for url in relaventURLs if url != 'NONE']

            if not filtered_url_list:
                return None
            else:
                return filtered_url_list   
    except Exception as e:
        print(f"An error occurred in LinksBreakUp: {str(e)}")
        return None
    
async def LinksBreakUp(api_key, token, url_prompt, linksString): # convert the list of links into a string and break it up into subarrays of 3000 tokens. It will break up some links but give better speed
    try:
        relaventURLs_list = []
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
                 "content": f"From the URLs below, delimted by three dashes(-), extract the URLs that are most relevant to the target information I provide. \
If there are no URLs that are relevant to the target information, refrain from returning any messages. Instead of returning any messages, only return 'NONE'. \
Otherwise, return no more than 10 URLs unless there are additional URLs that are still extremely relevant to the target information. Refrain from returning more than 15 URLs in total. \
The order of relevance is important. The first URL should be the most relevant. \
Refrain from generating any additional text associated with the URLs. Only return the URL in comma_seperated_list_of_url, for example: url1,url2,url3. Refrain from using any other format for the output. \
Refrain from returning any URL that is not relevant to the target information. If you are not sure if the URL is relevant, refrain from returning the URL.\n\n\
---\n{section}\n---"}]
            urlMessage = "Target Information:" + url_prompt
            relaventURLs_list.append(await singleGPT(api_key, messages,urlMessage, temperature=0.0, top_p=1))
        relaventURLs = ','.join(relaventURLs_list)
        return relaventURLs # return a text string of the links with potentially some text from GPT3.5
    except Exception as e:
        print(f"An error occurred in LinksBreakUp: {str(e)}")
        return None
    
def num_tokens_from_string(string: str, encoding_name = 'cl100k_base' ) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def truncate_text_tokens(text, encoding_name='cl100k_base', max_tokens=3000):
    """Truncate a string to have `max_tokens` according to the given encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    return encoding.encode(text)[:max_tokens]

#break up the content of long webpages into smaller chunks and pass each into GPT3.5 to avoid the token limit and return the summary of the whole webpage
async def pageBreakUp(api_key, content_prompt, content): 
    pageSummary = ''
    sectionNum = math.ceil(num_tokens_from_string(content) // 3000) + 1 
    cutoffIndex = math.ceil(len(content) // sectionNum)
    for i in range(sectionNum): #split the content into multiple section and use a new GPT3.5 for each section to avoid the token limit
        start_index = i * cutoffIndex
        end_index = (i + 1) * cutoffIndex
        section = content[start_index:end_index]
        section_messages = [
        {"role": "system", 
         "content": f"From the text below, delimted by three dashes(-), extract the information that are relevant to the target information I provide. \
You will start looking for the first target information from the text, and then look for the next target information until you finish looking for all the target information from the text.\n\
If the text does not contain any of the target information, refrain from summarizing the text. Instead of summarizing the task, only reply '4b76bd04151ea7384625746cecdb8ab293f261d4' \
Otherwise, for each target information, provide a summarization from the relevant text with as much detail as possible. Use the target information as the title of the summarization. \n\n\
---\n{section}\n---"}]
        pageMessage = "Target Informtion:\n"+ content_prompt
        pageSummary += await singleGPT(api_key, section_messages, pageMessage)
    if num_tokens_from_string(pageSummary) > 3000: #if the summary is still too long, truncate it to 3500 tokens
        pageSummary = truncate_text_tokens(pageSummary)
    return pageSummary

async def PageResult(api_key, content_prompt, content):
    pageSummary = ''
    if num_tokens_from_string(content) <= 3500: #if the content is less than 3500 tokens, pass the whole content to GPT
        messages = [
        {"role": "system", 
         "content": f"From the text below, delimted by three dashes(-), extract the information that are relevant to the target information I provide. \
You will start looking for the first target information from the text, and then look for the next target information until you finish looking for all the target information from the text.\n\
If the text does not contain any of the target information, refrain from summarizing the text. Instead of summarizing the task, only reply '4b76bd04151ea7384625746cecdb8ab293f261d4' \
Otherwise, for each target information, provide a summarization from the relevant text with as much detail as possible. Use the target information as the title of the summarization. \n\n\
---\n{content}\n---"}]
        pageMessage = "Target Informtion:\n" + content_prompt
        pageSummary = await singleGPT(api_key, messages, pageMessage)
    else: #split the webpage content into multiple section to avoid the token limit
        pageSummary = await pageBreakUp(api_key, content_prompt, content) #split the webpage content into multiple section and return the summary of the whole webpage
        #print("pageSummary: ",pageSummary)
        messages = [
        {"role": "system", 
         "content": f"From the text below, delimted by three dashes(-), extract the information that are relevant to the target information I provide. \
You will start looking for the first target information from the text, and then look for the next target information until you finish looking for all the target information from the text.\n\
If the text does not contain any of the target information, refrain from summarizing the text. Instead of summarizing the task, only reply '4b76bd04151ea7384625746cecdb8ab293f261d4' \
Otherwise, for each target information, provide a summarization from the relevant text with as much detail as possible. Use the target information as the title of the summarization. \n\n\
---\n{pageSummary}\n---"}]
        pageSummary = "Target Informtion:\n" + content_prompt
        pageSummary = await singleGPT(api_key, messages, pageSummary)

    return pageSummary

def getWebpageData(soup):
    for script in soup(['script', 'style']):# Remove any unwanted elements, such as scripts and styles, which may contain text that you don't want to extract
        script.decompose()
    text_content = soup.get_text(separator=' ') # Extract all the text content using the get_text() method
    clean_text = ' '.join(text_content.split()) # Clean up the extracted text by removing extra whitespace, line breaks, and other unnecessary characters
    # find all the links in the page
    title_tag = soup.find('title')
    page_Title = title_tag.text if title_tag else None
    return clean_text, page_Title

def getWebpageLinks(soup, searchDomain, url):
    links = []
    for a_tag in soup.find_all('a'):
        link = a_tag.get('href')
        if link:
            link, _ = urldefrag(link) # Remove the fragment from the URL
            absolute_url = urljoin(url, link)
            if absolute_url not in links: # Check if the URL is not already in the list since defrag can produce duplicates
                if searchDomain == None:
                    links.append(absolute_url)
                elif searchDomain != None and Url(absolute_url).is_from_domain(searchDomain):
                    links.append(absolute_url)
    return links

async def updateExcel(task_id, excelsheet, data):
    folder_path = 'Results'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    file_name = f"{folder_path}/{task_id}.xlsx"  # Create the Excel file name
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
        #     await asyncio.to_thread(writer.save)
        # else:  # If the sheet doesn't exist, write the new data as a new sheet
        #     writer = await asyncio.to_thread(pd.ExcelWriter, file_name, mode='a')
        #     await asyncio.to_thread(data.to_excel, writer, sheet_name=excelsheet, index=False)
        #     await asyncio.to_thread(writer.save)
            workbook = writer.book
            await asyncio.to_thread(workbook.save, file_name)
        else:  # If the sheet doesn't exist, write the new data as a new sheet
            writer = await asyncio.to_thread(pd.ExcelWriter, file_name, mode='a')
            await asyncio.to_thread(data.to_excel, writer, sheet_name=excelsheet, index=False)
            workbook = writer.book
            await asyncio.to_thread(workbook.save, file_name)
    else:  # If the file doesn't exist, write the new data as a new sheet
        await asyncio.to_thread(data.to_excel, file_name, sheet_name=excelsheet, index=False)
    return file_name

def get_domain(url):
    parts = urlparse(url)
    if not parts.scheme:
        # Add default scheme (http) if it's missing
        url = "http://" + url
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

def getContentPrompt(query_list):
    content_prompt = "\n".join(f"{i+1}. {obj}" for i, obj in enumerate(query_list))
    return content_prompt

def getURLPrompt(query_list):
    url_prompt = ", ".join([f"{obj}" for obj in query_list])
    return url_prompt

async def createSearchQuery(userAsk): # currently not used
    messages = [
                {"role": "system", 
                 "content": "Generate less than 4 Google search queries that reflect the search content in the Text provide. \
For each query, utilize specific keywords that accurately represent the topic of the Text. Refrain from creating related queries that are outside of text's search content. \
Ensure all queries are mutually exclusive and collectively exhaustive regarding the text's search content. \
Return the search queries in the format of comma_separated_list_of_queries. Refrain from numbering each item in the list. refrain from creating query in a new line. Refrain from creating queries with only one word. \
Example result format: query1, query2, query3, query4 "}]
    
    queryMessage = "Text:\n" + userAsk
    googleQueries = await singleGPT(messages, queryMessage, temperature=0.0, top_p=1, )
    # print(googleQueries)
    query_list = [query.strip() for query in googleQueries.split(',')] # remove the white space from the string and convert the string into a list
    # print(query_list)
    # input('Press Enter to continue...')
    return query_list