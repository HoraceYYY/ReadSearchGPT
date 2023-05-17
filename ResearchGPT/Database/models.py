from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import uuid

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()))
    start_time = Column(String)
    time_spent = Column(String)
    file_path = Column(String)
