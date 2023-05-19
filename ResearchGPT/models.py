from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    status = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime, default=None)
    time_spent = Column(String)
    file_path = Column(String)

class URLData(Base):
    __tablename__ = "url_data"

    task_id = Column(String, ForeignKey('tasks.id'), primary_key=True)
    url = Column(String)  # URL for all types of content
    title = Column(String)  # Title for 'Related' and 'Unrelated' categories
    content = Column(Text)  # In case content can be quite long for 'Related' and 'Unrelated' categories
    category = Column(String)  # Can be 'Related', 'Unrelated', or 'Unchecked Material'
    pdfs = Column(String)  # PDF links for 'Unchecked Material' category
    additional_links = Column(String)  # Additional Links for 'Unchecked Material' category

    task = relationship("Task", back_populates="url_data", uselist=False)

Task.url_data = relationship("URLData", back_populates="task", uselist=False)
