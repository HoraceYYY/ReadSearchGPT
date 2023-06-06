from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    topic = Column(String)
    status = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime, default=None)
    time_spent = Column(String)
    file_availability = Column(String, default="Available")
    file_path = Column(String)
    
    url_data = relationship("URLData", back_populates="task")
    email = relationship("Email", back_populates="task")

class URLData(Base):
    __tablename__ = "url_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_id = Column(String, ForeignKey('tasks.id'), nullable=False)
    url = Column(String)  # URL for all types of content
    title = Column(String)  # Title for 'Related' and 'Unrelated' categories
    content = Column(Text)  # In case content can be quite long for 'Related' and 'Unrelated' categories
    category = Column(String)  # Can be 'Related', 'Unrelated', or 'Unchecked Material'
    pdfs = Column(String)  # PDF links for 'Unchecked Material' category
    additional_links = Column(String)  # Additional Links for 'Unchecked Material' category

    task = relationship("Task", back_populates="url_data", uselist=False)

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    feedback = Column(Text)  # User's feedback on the product
    timestamp = Column(DateTime, default=func.now())  # The time when feedback was submitted

class Email(Base):
    __tablename__ = "email"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    research_id = Column(String, ForeignKey('tasks.id'), nullable=False)  # link to the task id
    email = Column(String)
    status = Column(Boolean, default=True)  # True = in use, False = not in use

    task = relationship("Task", back_populates="email")