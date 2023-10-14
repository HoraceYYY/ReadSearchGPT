from sqlalchemy.orm import Session
import models

def create_research(db: Session, userid):
    task = models.Task(userid=userid)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def create_queries(db: Session, task_id, search_queries):
    queries = models.Query()
    for query in search_queries:
        db_query = queries(task_id = task_id, query = query)
        db.add(db_query)
    db.commit()
    return


def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def delete_task(db: Session, task_id: str):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return True

def get_all_tasks(db: Session):
    return db.query(models.Task).all()

def update_task(db: Session, task_id: str, updated_info: dict):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        return None

    for key, value in updated_info.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
