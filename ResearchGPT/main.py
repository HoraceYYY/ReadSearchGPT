from Google import async_google
from aiohttp import ClientSession
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import asyncio, uuid, time,os
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware # to allow CORS
from datetime import datetime, timedelta
from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import and_
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

class FeedbackBase(BaseModel):
    feedback: str

app = FastAPI()

# Get a db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:5173",  
    "https://readsearch.azurewebsites.net",
    "www.readsearchgpt.com",
    "https://readsearchgpt.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search") # this is the entry point of the search 
async def startSearching(background_tasks: BackgroundTasks, search: Search, db: Session = Depends(get_db)):
    task_id = str(uuid.uuid4())
    # file_path = await create_output_excel_file(task_id)
    start_time = datetime.now()

    task = models.Task(id=task_id, topic=str(search.searchqueries),start_time=start_time, file_path=None, status="Researching...")     # Add your task to the database
    crud.create_task(db, task)
    # Use the existing session to create a new one for the background task
    background_tasks.add_task(run_task, task_id, search)
    return {"Research ID": task_id, "Research Topic(s)":str(search.searchqueries), "Status": "Researching...", "Start Time": str(start_time).split('.')[0], "Search Results": "Available"}

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
        return {"Research ID": task_id, "Research Topic(s)":task.topic, "Status": task.status, "Search Result": task.file_availability, "Start Time": task.start_time.strftime("%Y-%m-%d %H:%M:%S"), "Time Spent": task.time_spent}
    else:
        return {"Status": "Error", "Message": "Research not found"}
  
@app.post("/task/{task_id}/stop")
async def stop_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task:
        if task.status == "Researching...":
            task.status = "Cancelled"
            task.end_time = datetime.now()
            task.time_spent = str(task.end_time - task.start_time).split('.')[0]
            db.commit()
            return {"Status": "Research has been cancelled"}
        else:
            return {"message": "Search was not running."}
    else:
        return {"Status": "Error", "Message": "Research not found"}


async def download_excel(task_id: str, db):
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
            related = pd.concat([related, pd.DataFrame([{'URL': url_data.url, 'Title': url_data.title, 'Content': url_data.content}])], ignore_index=True)
        elif url_data.category == 'Unrelated':
            unrelated = pd.concat([unrelated, pd.DataFrame([{'URL': url_data.url, 'Title': url_data.title, 'Content': url_data.content}])], ignore_index=True)
        elif url_data.category == 'Unchecked Material':
            unchecked = pd.concat([unchecked, pd.DataFrame([{'PDFs': url_data.pdfs, 'Additional Links': url_data.additional_links}])], ignore_index=True)
    
    file_path = f"Results/{task_id}.xlsx"
    # Write data to Excel file with each DataFrame as a separate sheet
    with pd.ExcelWriter(file_path) as writer:
        related.to_excel(writer, sheet_name='Related', index=False)
        unrelated.to_excel(writer, sheet_name='Unrelated', index=False)
        unchecked.to_excel(writer, sheet_name='Unchecked Material', index=False)
    return file_path

@app.get("/task/{task_id}/webdownload")
async def web_download_excel(task_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    file_path = await download_excel(task_id, db)
    background_tasks.add_task(delete_file_after_delay, file_path, delay=60) # Add a background task to delete the file after 1 minute
    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=f"{task_id}.xlsx")     # Return the file as a response

def delete_file_after_delay(file_path: str, delay: int):
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)

class EmailRequest(BaseModel):
    research_id: str
    emails: List[str]

@app.post("/add_email")
async def add_email(email_request: EmailRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    research_id=email_request.research_id
    emails=email_request.emails
    print(research_id)
    print(emails)
    task = db.query(models.Task).filter(models.Task.id == research_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Research not found")
    
    old_emails = db.query(models.Email).filter(
        models.Email.research_id == research_id,
        models.Email.status == True
    ).all()
    for old_email in old_emails:
        old_email.status = False

    for email in emails:
        new_email = models.Email(research_id=research_id, email=email, status=True)
        db.add(new_email)
    
    db.commit()

    if task.status in ["Completed", "Cancelled"] and task.file_availability == "Available":
        file_path = await download_excel(research_id, db)
        user = 'henryyu.business@gmail.com'
        password = "gaoshou123"
        header = "Your ReadSearch Results Are Ready"
        message = f"Please see attached results for the following search topic. \n\nResearch Topic: {task.topic}. \n\nPlease use the following Research ID if you wish to download the result again within the next 24 hours: {task.id} \n\n Thank you for using ReadSearchGPT!"
        background_tasks.add_task(send_email_outlook, user, password, emails, header, message, file_path)
        background_tasks.add_task(delete_file_after_delay, file_path, delay=60)
        
def send_email_outlook(user, password, mail_to, subject, message, file_path):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = ', '.join(mail_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = os.path.basename(file_path)
    attachment = open(file_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(user, password)
    text = msg.as_string()
    server.sendmail(user, mail_to, text)
    server.quit()
    
@app.post("/task/cleanup")
async def cleanup(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_cleanup)
    return {"Status": "Cleanup started"}

async def run_cleanup():
    db = SessionLocal()  # Create a new session
    try:
        # Find tasks that ended more than 24 hours ago
        old_tasks = db.query(models.Task).filter(
            and_(models.Task.end_time < datetime.now() - timedelta(hours=24), 
                 models.Task.file_availability == "Available")).all()
        for task in old_tasks:
            # Delete URL data associated with the task
            db.query(models.URLData).filter(models.URLData.task_id == task.id).delete()
            # Update file_availability status in the Task table
            task.file_availability = "Expired"
        
        # Commit the changes to the database
        db.commit()
    finally:    
        db.close()

@app.get("/task/get_all_tasks")
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    return {"Tasks": [dict(task_id=task.id, status=task.status, start_time=task.start_time, time_spent=task.time_spent, file_path=task.file_path) for task in tasks]}

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

@app.post("/feedback")
async def create_feedback(feedback: FeedbackBase, db: Session = Depends(get_db)):
    new_feedback = models.Feedback(
        feedback=feedback.feedback
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return {"Message": "Feedback successfully submitted", "Feedback ID": new_feedback.id}
