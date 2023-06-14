from Google import async_google
from aiohttp import ClientSession
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import asyncio, uuid, time,os, ast, smtplib
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

class EmailRequest(BaseModel):
    research_id: str
    emails: List[str]

class APIKey(BaseModel):
    apiKey: str

class additionalSearch(BaseModel):
    queryID: str
    apiKey: str

class firstSearch(BaseModel):
    searchqueries: List[str]
    searchDomain: str | None = None
    apiKey: str

class deepsearch(BaseModel):
    queryID: str
    searchDomain: str | None = None
    apiKey: str

class FeedbackBase(BaseModel):
    feedback: str

app = FastAPI()

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
# Get a db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/firstsearch") # this is the entry point of the search, this will search all the topics entered
async def first_search(search: firstSearch, db: Session = Depends(get_db)):
    try:
        searchqueries = search.searchqueries
        userDomain = search.searchDomain
        api_key = search.apiKey
        research_id, querywithresult = await async_google.first_search(db, searchqueries, userDomain, api_key)
        db.commit()
        print(f"Task Completed")
    finally:    
        db.close()
    return research_id, querywithresult

@app.post("/secondsearch")
async def second_search(search: additionalSearch, db: Session = Depends(get_db)):
    try:
        queryid = search.queryID
        api_key = search.apiKey
        querywithresult = await async_google.second_search(db, queryid, api_key) # this results includes the initial search as well
        db.commit()
        print(f"Task Completed")
    finally:
        db.close()
    return querywithresult

@app.post("/firstdeepsearch")
async def first_deep_search(search: deepsearch, db: Session = Depends(get_db)):
    try:
        queryid = search.queryID
        userDomain = search.searchDomain
        api_key = search.apiKey
        querywithresult = await async_google.first_deep_search(db, queryid, userDomain, api_key) # this results includes the initial search as well
        db.commit()
        print(f"Task Completed")
    finally:
        db.close()
    return querywithresult

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

@app.post("/add_email")
async def add_email(email_request: EmailRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    research_id=email_request.research_id
    emails=email_request.emails
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
        user, password, header, message, file_path = await draft_email(research_id, task, db)
        success, error_msg = send_email(user, password, emails, header, message, file_path)
        background_tasks.add_task(delete_file_after_delay, file_path, delay=60)
        if not success:
            return print("Email sending failed with error:", error_msg)
        return print("Email sent")

async def draft_email(research_id, task, db): ## update email to the readsearch domain
    file_path = await download_excel(research_id, db)
    user = 'readsearchgpt@gmail.com'
    password = "cqrdmoxaeduoqxtj"
    header = f"Your ReadSearch Results Are Ready - Research ID: {research_id}"
    topic_list = ast.literal_eval(task.topic)
    topics = '\n'.join(f'{i+1}. {topic}' for i, topic in enumerate(topic_list))
    message = f"Please see attached results for the following research topics: \n{topics}. \n\nPlease use your Research ID if you wish to download the result again within the next 24 hours. Thank you for using ReadSearchGPT!"
    return user, password, header, message, file_path
        
def send_email(user, password, mail_to, subject, message, file_path):
    try:
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
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        text = msg.as_string()
        server.sendmail(user, mail_to, text)
        server.quit()

        return True, ""

    except Exception as e:
        return False, str(e)

    
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
