from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base

"""
local database vs GCP database. Only choose one
"""
##SQLALCHEMY_DATABASE_URL = "postgresql://readsearch:readsearch@localhost:5432/tasks"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:readsearchpostgres@34.66.209.78:5432/tasks"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
