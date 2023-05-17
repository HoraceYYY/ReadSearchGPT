from sqlalchemy.orm import Session
import models

def create_task(db: Session, task: models.Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

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