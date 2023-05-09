import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from data import *
from prompts import pipeline
from utils import document_store, retriever
from models import *
from sqlmodel import Session, select, delete
app = FastAPI()

@app.on_event("startup")
#create db and tables
def on_startup():
    create_db_and_tables()




# Endpoint to inject documents
@app.post("/doc_ingestion")
def add_documents(doc: DocModel):
    docs = read_data(doc.dir_path)
    docs = preprocess(docs)
    document_store.write_documents(docs, duplicate_documents='skip')
    document_store.update_embeddings(retriever=retriever(doc.api_key), update_existing_embeddings=False)
    return JSONResponse(content={"message": "Documents added successfully"})


# Endpoint for user query
@app.post("/query")
def query(query: QueryModel):
    # first check, do we have conversation for the session
    # if yes, first get that memory
    working_memory = load_history(query.session_id)
    if len(working_memory) == 0:
        #if no, create an empty memory
        working_memory =[]
    memory_utils = pipeline(query.api_key, working_memory)
    results = memory_utils.chat(query.text)
    answer = results['answers'][0].answer
    save_sess_db(query.session_id,
                 query.text,
                 answer)
    return {'answer': answer}

@app.post("/delete")
def delete_session(session:DeleteSession):
    """
    Deletes a session from the database.
    """
    session_id=session.session_id
    if session_id  is None:
        raise HTTPException(status_code=404, detail="Please provide session id")

    with Session(engine) as session:

        # if session id and client id is given then delete the particular session from the query database 
        if session_id:
            query = delete(QueryDB).where(QueryDB.session_id == session_id)
            result = session.execute(query)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail=f"Session id {session_id} not found")
            session.commit()
            return {'message':f"Session id {session_id} Deleted"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)