from Google import async_google
from Google import async_utils
import time, asyncio, uuid, os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from enum import Enum
from typing import List
import pandas as pd

class DepthLevel(str, Enum):
    quick = "quick"
    thorough = "thorough"
    deep = "deep"

class Search(BaseModel):
    topic: str
    objectives_inputs: List[str]
    searchDomain: str | None = None
    max_depth: DepthLevel = DepthLevel.quick  # Use the DepthLevel Enum

    _depth_mapping = {
        DepthLevel.quick: 1,
        DepthLevel.thorough: 2,
        DepthLevel.deep: 3,
    }

    def get_depth_value(self):
        return self._depth_mapping.get(self.max_depth, None)

app = FastAPI()
tasks = {} # this is only a temp solution, it is in memory and not scalable. if system crash, all info in this array will be lost

@app.post("/search/")
async def startSearching(background_tasks: BackgroundTasks, search: Search):
    task_id = str(uuid.uuid4())
    file_path = await create_output_excel_file(task_id, search.topic)
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
    topic = search.topic
    objectives_inputs = search.objectives_inputs
    userDomain = search.searchDomain
    max_depth = search.get_depth_value()  # Get the integer value of max_depth

    await asyncio.create_task(async_google.main(tasks[task_id], task_id, topic, objectives_inputs, userDomain, max_depth))
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["execution_time"] = execution_time


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