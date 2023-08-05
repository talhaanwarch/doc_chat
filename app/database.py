from sqlalchemy import Column, Integer, String, create_engine, delete, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .utils import get_settings


Base = declarative_base()


# Retrieve the PostgreSQL credentials from environment variables
db_host = get_settings().postgres_host
db_port = get_settings().postgres_port
db_name = get_settings().postgres_db
db_user = get_settings().postgres_user
db_password = get_settings().postgres_password

# Construct the PostgreSQL URL
postgresql_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


# Replace the connection string with your PostgreSQL details
# postgresql_url = "postgresql://postgres:talha1234@localhost:5432/sparkdb"
engine = create_engine(postgresql_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)



class QueryDB(Base):
    __tablename__ = "querydb"

    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    client_id = Column(String)
    query = Column(String)
    answer = Column(String)
    
    total_tokens = Column(Integer)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_cost = Column(Float)

def create_db_and_tables():
    # Base.metadata.drop_all(bind=engine) # TODO getting fupicate error
    Base.metadata.create_all(bind=engine)

