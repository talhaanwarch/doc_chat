from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import MilvusDocumentStore

document_store = MilvusDocumentStore(
    embedding_dim=1536,
    duplicate_documents='skip',
    sql_url="sqlite:///mydb.db")


def retriever(api_key):
    return EmbeddingRetriever(
        document_store=document_store,
        embedding_model="text-embedding-ada-002",
        api_key=api_key,
        max_seq_len=1024,
        top_k=4,
        )