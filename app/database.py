from sqlalchemy import Column, Integer, String, create_engine, delete, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Replace the connection string with your PostgreSQL details
postgresql_url = "postgresql://postgres:talha1234@localhost:5432/sparkdb"
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
