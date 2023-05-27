from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
# from dotenv import load_dotenv
# import os

# dotenv_path = os.path.join(os.path.dirname(__file__), 'Google', '.env')
# load_dotenv(dotenv_path)  # Load the .env file

##SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://postgres:readsearchpostgres@/tasks?unix_sock=/cloudsql/readsearch:us-central1:readsearchubc/.s.PGSQL.5432"
SQLALCHEMY_DATABASE_URL = "postgresql://progresql:kavfa0-ramkEg-jaxmid@readsearchdb.postgres.database.azure.com/postgres?sslmode=require"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
