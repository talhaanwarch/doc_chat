import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from models import DocModel, QueryModel, DeleteSession
from database import QueryDB, create_db_and_tables
from vector_database import vector_db, db_conversation_chain
from data import load_n_split
from utils import count_tokens
from chat_session import ChatSession

app = FastAPI()
chat_session = ChatSession()

@app.on_event("startup")
def on_startup():
    """
    Event handler called when the application starts up.
    """
    create_db_and_tables()


@app.post("/doc_ingestion")
def add_documents(doc: DocModel):
    """
    Endpoint to add documents for ingestion.
    """
    docs = load_n_split(doc.dir_path)
    _ = vector_db(docs, collection_name=doc.collection_name)
    return JSONResponse(content={"message": "Documents added successfully"})


@app.post("/query")
def query(query: QueryModel):
    """
    Endpoint to process user queries.
    """
    # Check if there is a conversation history for the session
    working_memory = chat_session.load_history(query.session_id)
    if len(working_memory) == 0:
        working_memory = None
    
    # Get conversation chain
    chain = db_conversation_chain(working_memory, collection_name=query.collection_name)
    result, cost = count_tokens(chain, query.text)

    # Save memory to disk
    answer = result['answer']
    chat_session.save_sess_db(query.session_id, query.text, answer)
    return {'answer': answer, "cost": cost}


@app.post("/delete")
def delete_session(session: DeleteSession):
    """
    Endpoint to delete a session from the database.
    """
    response = chat_session.delete_sess_db(session.session_id)
    return response
   


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
