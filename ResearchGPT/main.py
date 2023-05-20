from Google import async_google, async_utils
from aiohttp import ClientSession
import asyncio, uuid
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware # to allow CORS
from datetime import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
import models, crud

class SearchRequest(BaseModel): # currently not used
    userAsk: str

class APIKey(BaseModel):
    apiKey: str

class Search(BaseModel):
    searchqueries: List[str]
    searchDomain: str | None = None
    max_depth: int  # 0 - 3 Use the DepthLevel Enum
    searchWidth: int # 1-10
    apiKey: str

app = FastAPI()

# Get a db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        searchqueries = await async_utils.createSearchQuery(searchrequest.userAsk,)
        return {"success": True, "data": searchqueries}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/search/") # this is the entry point of the search 
async def startSearching(background_tasks: BackgroundTasks, search: Search, db: Session = Depends(get_db)):
    task_id = str(uuid.uuid4())
    # file_path = await create_output_excel_file(task_id)
    start_time = datetime.now()

    task = models.Task(id=task_id, start_time=start_time, file_path=None, status="Researching...")     # Add your task to the database
    crud.create_task(db, task)
    # Use the existing session to create a new one for the background task
    background_tasks.add_task(run_task, task_id, search)
    return {"Task ID": task_id, "Status": "Research has started"}

async def run_task(task_id: str, search: Search):
    db = SessionLocal()  # Create a new session
    try:
        searchqueries = search.searchqueries
        userDomain = search.searchDomain
        max_depth = search.max_depth  # Get the integer value of max_depth
        searchWidth = search.searchWidth
        api_key = search.apiKey
        
        await asyncio.create_task(async_google.main(task_id, searchqueries, userDomain, max_depth, searchWidth, api_key))
        task = crud.get_task(db, task_id)
        end_time = datetime.now()
        execution_time = end_time - task.start_time
        if task.status == "Researching...":
            task.status = "Completed"
        task.time_spent = str(execution_time).split('.')[0]
        task.end_time = end_time
        db.commit()
        print(f"Task Completed in {execution_time}")
    finally:    
        db.close()

# async def create_output_excel_file(task_id):
#     folder_path = 'Results'
#     os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
#     file_name = f"{folder_path}/{task_id}.xlsx"  # Create the Excel file name
#     return file_name

@app.get("/task/{task_id}/status")
async def task_status(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task:
        #check status
        if task.status == "Researching...":
            current_time = datetime.now()
            elapsed_time = current_time - task.start_time
            task.time_spent = str(elapsed_time).split('.')[0]
            db.commit()
        return {"Task ID": task_id, "Status": task.status, "Start Time": task.start_time.strftime("%Y-%m-%d %H:%M:%S"), "Time Spent": task.time_spent}
    else:
        return {"Status": "Error", "Message": "Task not found"}
  
@app.post("/task/{task_id}/stop")
async def stop_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task:
        task.status = "Cancelled"
        task.end_time = datetime.now()
        task.time_spent = str(task.end_time - task.start_time).split('.')[0]
        db.commit()
        return {"Status": "Task has been cancelled"}
    else:
        return {"Status": "Error", "Message": "Task not found"}

@app.get("/task/{task_id}/download")
async def download_excel(task_id: str, db: Session = Depends(get_db)):
    # Find the URL data for the specified task ID
    url_data_list = db.query(models.URLData).filter(models.URLData.task_id == task_id).all()

    if not url_data_list:
        raise HTTPException(status_code=404, detail="Task not found")

    # Create data frames for each category
    related = pd.DataFrame(columns=['URL', 'Title', 'Content'])
    unrelated = pd.DataFrame(columns=['URL', 'Title', 'Content'])
    unchecked = pd.DataFrame(columns=['PDFs', 'Additional Links'])

    for url_data in url_data_list:
        if url_data.category == 'Related':
            related = related.append({'URL': url_data.url, 'Title': url_data.title, 'Content': url_data.content}, ignore_index=True)
        elif url_data.category == 'Unrelated':
            unrelated = unrelated.append({'URL': url_data.url, 'Title': url_data.title, 'Content': url_data.content}, ignore_index=True)
        elif url_data.category == 'Unchecked Material':
            unchecked = unchecked.append({'PDFs': url_data.pdfs, 'Additional Links': url_data.additional_links}, ignore_index=True)

    # Write data to Excel file with each DataFrame as a separate sheet
    with pd.ExcelWriter(f"Results/{task_id}.xlsx") as writer:
        related.to_excel(writer, sheet_name='Related', index=False)
        unrelated.to_excel(writer, sheet_name='Unrelated', index=False)
        unchecked.to_excel(writer, sheet_name='Unchecked Material', index=False)

    return {f"Results/{task_id}.xlsx"}
    
@app.post("/task/{task_id}/deletefile")
async def delete_excel(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task:
        task.status = "Deleted"
        db.commit()
        return {"Status": "Excel file has been deleted"}
    else:
        return {"Status": "Error", "Message": "Task not found"}

@app.get("/task/get_all_tasks")
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    return {"Tasks": [dict(task_id=task.id, status=task.status, start_time=task.start_time, time_spent=task.time_spent, file_path=task.file_path) for task in tasks]}

@app.post("/test")
def test(search: Search):
    # print the body of the request and their data type
    print(search)
    # print the data type of each field
    print(type(search.searchqueries))
    print(type(search.searchDomain))
    print(type(search.max_depth))
    print(type(search.searchWidth))
    print(type(search.apiKey))

    return {"Task ID":"sudo task id" , "Status": "Task has started", "File Path": "sudo file path"}

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
                    return {"Key": "Valid"}
                else:
                    print("error: ", status_code)
                    return {"Key": f"Not Valid: {status_code}"}
        except Exception as e:
            print(e)
            return {"Key": f"Not Valid: {e}"}

