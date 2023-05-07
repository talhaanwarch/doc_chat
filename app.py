import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from data import *
from prompts import pipeline
from utils import document_store, retriever
from models import *
app = FastAPI()



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
    print('working_memory',query.working_memory)
    memory_utils, working_memory = pipeline(query.api_key, query.working_memory)
    results = memory_utils.chat(query.text)
    answer = results['answers'][0].answer
    return {'answer': answer, "working_memory":working_memory}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)