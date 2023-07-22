from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import JSONResponse
import shortuuid
import structlog
from time import time

from .schema import DocModel, QueryModel, DeleteSession
from .database import create_db_and_tables
from .vector_database import vector_database, db_conversation_chain
from .data import S3FileLoader
from .chat_session import ChatSession
from .utils import count_tokens, AttributeDict
from .aimodeldownload import *

logger = structlog.getLogger()

app = FastAPI()
chat_session = ChatSession()


@app.on_event("startup")
def on_startup():
    """
    Event handler called when the application starts up.
    """
    create_db_and_tables()
    app.state.llm = llm_model("gpt4all_light")
    app.state.embedding = get_embeddings()




@app.post("/doc_ingestion")
def add_documents(doc: DocModel, background_tasks: BackgroundTasks,  request: Request):
    """
    Endpoint to add documents for ingestion.
    """
    background_tasks.add_task(process_documents, doc, request)
    return JSONResponse(content={"message": "Documents ingestion process started"})

def process_documents(doc: DocModel, request: Request):
    docs = S3FileLoader().load_and_split(doc.urls)
    _ = vector_database(
        doc_text=docs,
        collection_name=shortuuid.uuid(doc.client_id),
        embeddings=request.app.state.embedding
    )


@app.post("/query")
def query_response(query: QueryModel, request: Request):
    """
    Endpoint to process user queries.
    """
    # Check if there is a conversation history for the session
    stored_memory = chat_session.load_history(query.session_id)
    if len(stored_memory) == 0:
        stored_memory = None

    # Get conversation chain
    chain = db_conversation_chain(
        stored_memory=stored_memory,
        llm_model=request.app.state.llm,
        embeddings = request.app.state.embedding,
        collection_name=shortuuid.uuid(query.client_id)
    )

    if query.llm_name == 'openai':
        result, cost = count_tokens(chain, query.text)
        
    else:
        start = time()
        result = chain(query.text)
        end = time()
        total = round((end - start),3)
        logger.info(f'time for one query {total}')
        cost = AttributeDict({ #TODO atleasr get total number of tokens
            "total_tokens": 0, 
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_cost": 0
        })

    sources = list(set([doc.metadata['source'].split('/')[-1] for doc in
                        result['source_documents']]))
    answer = result['answer']
    chat_session.save_sess_db(shortuuid.uuid(query.client_id), 
                              query.session_id, query.text, answer, cost)

    return {
        'answer': answer,
        "cost": cost,
        'source': sources
    }


@app.post("/delete")
def delete_session(session: DeleteSession):
    """
    Endpoint to delete a session from the database.
    """
    response = chat_session.delete_sess_db(session.session_id)
    return response
