from pydantic import BaseModel, validator
from typing import Optional
from fastapi import HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os
import re

def validate_uuid(uuid_string):
    pattern = re.compile(
        r'^[0-9a-fA-F]{8}-'
        r'[0-9a-fA-F]{4}-'
        r'[0-9a-fA-F]{4}-'
        r'[0-9a-fA-F]{4}-'
        r'[0-9a-fA-F]{12}$'
        )
    return re.match(pattern, uuid_string)


class DocModel(BaseModel):
    api_key: str
    dir_path: str

    @validator('api_key')
    def validate_api_key(cls, api_key):
        # Perform your validation logic here
        if (len(api_key) != 51) or not api_key.startswith('sk'):
            raise ValueError('The API is not valid')
        return api_key

    @validator('dir_path')
    def validate_dir_path(cls, dir_path):
        # Perform your validation logic here
        if not os.path.exists(dir_path):
            raise ValueError('Directory path must start with a forward slash')
        return dir_path

class QueryModel(BaseModel):
    api_key: str
    text: str
    session_id: str

    @validator('api_key')
    def validate_api_key(cls, api_key):
        if len(api_key) != 51:
            raise ValueError('API key must be 51 characters long')
        if not api_key.startswith('sk'):
            raise ValueError('API key must start with "sk"')
        return api_key

    @validator('text')
    def validate_text(cls, text):
        if not text:
            raise ValueError('Text must be provided')
        return text

    @validator('session_id')
    def validate_session_id(cls, session_id):
        if not validate_uuid(session_id):
            raise ValueError('Session ID must be in uuid4 format')
        return session_id



class DeleteSession(BaseModel):
    session_id: str
    @validator('session_id')
    def validate_session_id(cls, session_id):
        if not validate_uuid(session_id):
            raise ValueError('Session ID must be in uuid4 format')
        return session_id


class QueryDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    query: str
    answer: str
    session_id: str # TODO uuid


    
sqlite_file_name = "mydb.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args) 
# Because we created the engine with echo=True, it will print out all the SQL code that it is executing:

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)



def load_history(session_id):
        """
        Loads a chat session from the database and returns a list of the 
        conversation

        :param data: session_id
        :return: List containing query and responses from the database
        """
        with Session(engine) as session:
            # Retrieve the conversation for the given session and client
            statement = f"SELECT * FROM querydb WHERE \
                session_id = '{session_id}'"
            # Execute the SQL statement to select all rows where the session and client match
            results = session.exec(statement)
            # Create a list from the result set
            results = [i for i in results]

        results = [i for j in results for i in j[1:-1]]
        # check if existing context is same as the new context on same session
        results = [item for item in results if item != "I don't have enough information to answer the question."]
        return results

def save_sess_db(session_id, query, answer):
    db = QueryDB(query=query, answer=answer, session_id=session_id)
    with Session(engine) as session:
        session.add(db)
        session.commit()
        session.refresh(db)


