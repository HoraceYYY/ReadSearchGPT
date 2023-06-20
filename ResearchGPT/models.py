from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Text, func, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    # One-to-many relationship with Query
    queries = relationship("Query", backref="task")

class Query(Base):
    __tablename__ = "queries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_id = Column(UUID, ForeignKey('tasks.id'), nullable=False)
    query = Column(String)
    # One-to-many relationship with URL and URLData
    urls = relationship("URL", backref="query")
    url_data = relationship("URLData", backref="query")
    url_data = relationship("URLSummary", backref="query")

class URL(Base):
    __tablename__ = "urls"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    query_id = Column(UUID, ForeignKey('queries.id'), nullable=False)
    source = Column(ARRAY(String))
    result = Column(ARRAY(String))


class URLData(Base):
    __tablename__ = "url_data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    query_id = Column(UUID, ForeignKey('queries.id'), nullable=False)
    url = Column(String)  # URL for all categories
    title = Column(String)  # Title for 'website content'
    content = Column(Text)  # Only for website content category
    category = Column(String)  # Can be 'Website_Content', 'Unread_Websites', or 'PDFs'

class URLSummary(Base):
    __tablename__ = "url_summary"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    query_id = Column(UUID, ForeignKey('queries.id'), nullable=False)
    summarytype = Column(String)
    summary = Column(String)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    feedback = Column(Text)  # User's feedback on the product
    timestamp = Column(DateTime, default=func.now())  # The time when feedback was submitted

class Email(Base):
    __tablename__ = "email"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String)
    status = Column(Boolean, default=True)  # True = in use, False = not in use

