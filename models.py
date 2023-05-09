from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
class DocModel(BaseModel):
    api_key: str
    dir_path: str

class QueryModel(BaseModel):
    api_key: str
    text: str
    session_id: str # TODO uuid

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


class DeleteSession(BaseModel):
    session_id: str

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


