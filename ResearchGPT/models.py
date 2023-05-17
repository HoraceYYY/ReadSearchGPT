from sqlalchemy import Column, String, DateTime
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    status = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime, default=None)
    time_spent = Column(String)
    file_path = Column(String)
