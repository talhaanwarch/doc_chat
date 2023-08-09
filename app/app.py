from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
import shortuuid
import structlog
import pytz
from time import time
from datetime import datetime, timezone
from .schema import DocModel, QueryModel
from .database import create_db_and_tables
from .vector_database import vector_database, db_conversation_chain
from .data import S3FileLoader
from .chat_session import ChatSession
from .utils import count_tokens

logger = structlog.getLogger()

app = FastAPI()
chat_session = ChatSession()


@app.on_event("startup")
def on_startup():
    """
    Event handler called when the application starts up.
    """
    create_db_and_tables()


@app.post("/doc_ingestion")
def add_documents(doc: DocModel, background_tasks: BackgroundTasks):
    """
    Endpoint to add documents for ingestion.
    """
    background_tasks.add_task(process_documents, doc)
    return JSONResponse(content={"message": "Documents ingestion process started"})

def process_documents(doc: DocModel):
    docs = S3FileLoader().load_and_split(doc.urls)
    _ = vector_database(
        doc_text=docs,
        collection_name=shortuuid.uuid(doc.client_id),
    )


@app.post("/query")
def query_response(query: QueryModel):
    """
    Endpoint to process user queries.
    """
    # Check if there is a conversation history for the session
    utc_time = datetime.utcnow()
    pkt_timezone = pytz.timezone('Asia/Karachi')
    date_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pkt_timezone)
    start = time()
    stored_memory = chat_session.load_history(query.session_id)
    if len(stored_memory) == 0:
        stored_memory = None

    # Get conversation chain
    chain = db_conversation_chain(
        stored_memory=stored_memory,
        collection_name=shortuuid.uuid(query.client_id)
    )

    result, cost = count_tokens(chain, query.text)
   
    
    sources = list(set([doc.metadata['source'].split('/')[-1] for doc in
                        result['source_documents']]))
    answer = result['answer']
    end = time()
    total_time = end - start 
    chat_session.save_sess_db(query.client_id, 
                              query.session_id, 
                              query.text, answer, cost,
                              date_time.strftime("%B %d, %Y"),
                              date_time.strftime("%H:%M:%S"),
                              round(total_time,2)
                                )
    
    logger.info(f" time taken {total_time}")
    return {
        'answer': answer,
        "cost": cost,
        'source': sources
    }
