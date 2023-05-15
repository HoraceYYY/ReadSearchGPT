from Google import async_google, async_utils
from aiohttp import ClientSession
import time, asyncio, uuid, os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware # to allow CORS
import openai


class SearchRequest(BaseModel): # currently not used
    userAsk: str

class APIKey(BaseModel):
    apiKey: str

class Search(BaseModel):
    searchqueries: List[str]
    searchDomain: str | None = None
    max_depth: int  # 0 - 3 Use the DepthLevel Enum
    searchWidth: int # 1-10


app = FastAPI()

origins = [
    "http://localhost:5173",  # assuming your Vue.js app is running on port 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = {} # this is only a temp solution, it is in memory and not scalable. if system crash, all info in this array will be lost

@app.post("/queries/") # currently not used
async def create_search_query(searchrequest: SearchRequest):
    try:
        searchqueries = await async_utils.createSearchQuery(searchrequest.userAsk)
        return {"success": True, "data": searchqueries}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/search/") # this is the entry point of the search 
async def startSearching(background_tasks: BackgroundTasks, search: Search):
    task_id = str(uuid.uuid4())
    file_path = await create_output_excel_file(task_id, 'results')
    tasks[task_id] = {"status": "running", "execution_time": None, "file_path": file_path}
    background_tasks.add_task(run_task, task_id, search)
    return {"task_id": task_id, "status": "Task has started", "file_path": file_path}

async def create_output_excel_file(task_id, excel_name):
    folder_path = f'Results/{task_id}'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    file_name = f"{folder_path}/{excel_name}.xlsx"  # Create the Excel file name
    if not os.path.isfile(file_name):  # Check if the file exists
        # If the file doesn't exist, create a new Excel file with 'Related' and 'Unrelated' sheets
        df_related = pd.DataFrame(columns=['URL', 'Title', 'Content'])
        df_unrelated = pd.DataFrame(columns=['URL', 'Title', 'Content'])
        with pd.ExcelWriter(file_name) as writer:
            df_related.to_excel(writer, sheet_name='Related', index=False)
            df_unrelated.to_excel(writer, sheet_name='Unrelated', index=False)

    return file_name

async def run_task(task_id: str, search: Search):
    start_time = time.time()
    searchqueries = search.searchqueries
    userDomain = search.searchDomain
    max_depth = search.max_depth  # Get the integer value of max_depth
    searchWidth = search.searchWidth

    await asyncio.create_task(async_google.main(tasks, task_id, searchqueries, userDomain, max_depth, searchWidth))
    
    end_time = time.time()
    execution_time = end_time - start_time
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["execution_time"] = execution_time
    print(f"Task Completed in {execution_time} seconds")


@app.get("/task/{task_id}/status")
async def task_status(task_id: str):
    if task_id in tasks:
        return tasks[task_id]
    else:
        return {"status": "error", "message": "Task not found"}
    
@app.post("/task/{task_id}/stop")
async def stop_task(task_id: str):
    if task_id in tasks:
        tasks[task_id]["status"] = "canceled"
        return {"status": "Task has been canceled"}
    else:
        return {"status": "error", "message": "Task not found"}

@app.get("/task/{task_id}/download")
async def download_excel(task_id: str):
    if task_id in tasks:
        return tasks[task_id]["file_path"]
    else:
        return {"status": "error", "message": "Task not found"}
    
@app.get("/task/{task_id}/delete")
async def delete_excel(task_id: str):
    if task_id in tasks:
        file_path = tasks[task_id]["file_path"]
        os.remove(file_path)
        tasks[task_id]["status"] = "deleted"
        return {"status": "Excel file has been deleted"}
    else:
        return {"status": "error", "message": "Task not found"}

@app.get("/task/get_all_tasks")
async def get_all_tasks():
    return tasks

@app.post("/test")
def test(search: Search):
    # print the body of the request and their data type
    print(search)
    # print the data type of each field
    print(type(search.searchqueries))
    print(type(search.searchDomain))
    print(type(search.max_depth))
    print(type(search.searchWidth))

@app.post("/testapi")
async def testAPI(apiKey: APIKey):
    api_key = apiKey.apiKey
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello!"}]
    }

    async with ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=body) as response:
                status_code = response.status
                if status_code == 200:
                    print("success: ", status_code)
                    return {"Open AI Key": "Valid"}
                else:
                    print("error: ", status_code)
                    return {"Open AI Key": f"Not Valid: {status_code}"}
        except Exception as e:
            print(e)
            return {"Open AI Key": f"Not Valid: {e}"}


# def testGPTAPI(apiKey: APIKey):
#     openai.api_key = apiKey.apiKey

#     completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "user", "content": "hello"}
#     ]
#     )
#     print(completion)
#     return completion["choices"][0]["message"]["content"]
