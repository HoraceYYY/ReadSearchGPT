from sqlalchemy.orm import Session
from . import models

def create_task(db: Session, task: models.Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
