from sqlalchemy import Column, Integer, String, create_engine, delete, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()


Base = declarative_base()


# Retrieve the PostgreSQL credentials from environment variables
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

# Construct the PostgreSQL URL
postgresql_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


# Replace the connection string with your PostgreSQL details
# postgresql_url = "postgresql://postgres:talha1234@localhost:5432/sparkdb"
engine = create_engine(postgresql_url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class QueryDB(Base):
    __tablename__ = "querydb"

    id = Column(Integer, primary_key=True)
    query = Column(String)
    answer = Column(String)
    session_id = Column(String)
    total_tokens = Column(Integer)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_cost = Column(Float)

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
