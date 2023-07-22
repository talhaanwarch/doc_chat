from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from fastapi import HTTPException
import pymilvus
from langchain.schema import messages_from_dict
import structlog

from .utils import get_settings
from .prompts import prompt_doc, prompt_chat


logger = structlog.getLogger()


def get_chat_history(inputs):
    """
    Get human input only
    """
    inputs = [i.content for i in inputs]
    # inputs = [string for index, string in enumerate(inputs) if index % 2 == 0]
    return '\n'.join(inputs)



def vector_database(collection_name, drop_existing_embeddings=False, embeddings=None, doc_text=None):
    """
    Creates and returns a Milvus database based on the specified parameters.
    Args:
        collection_name: The name of the collection.
        drop_existing_embeddings: Whether to drop existing embeddings.
        embeddings_name: The name of the embeddings ('openai' or 'sentence').
        doc_text: The document text.
    Returns:
        The Milvus database.
    """
    

    if doc_text:
        try:
            vector_db = Milvus.from_documents(
                doc_text,
                embeddings,
                collection_name=collection_name,
                drop_old=drop_existing_embeddings,
                connection_args={"host": get_settings().milvus_host, "port": "19530"},
                # if we want to communicate between two dockers then instead of localhost
                # we need to use milvus-standalone
            )
            logger.info("Successfully added")
        except pymilvus.exceptions.ParamError:
            raise HTTPException(status_code=400,
                                detail=f"collection_name {collection_name} already exists. Either set drop_existing_embeddings to true or change collection_name")
    else:
        vector_db = Milvus(
            embeddings,
            collection_name=collection_name,
            connection_args={"host": get_settings().milvus_host, "port": "19530"},
        )
    return vector_db






def db_conversation_chain(llm_model, embeddings, stored_memory, collection_name):

    """
    Creates and returns a ConversationalRetrievalChain based on the specified parameters.
    Args:
        llm_name: The name of the language model ('openai', 'gpt4all', or 'llamacpp').
        stored_memory: Existing conversation.
        collection_name: The name of the collection (optional).
    Returns:
        The ConversationalRetrievalChain.
    """

   



    vector_db = vector_database(
        collection_name=collection_name,
        embeddings=embeddings
        )

    if stored_memory:
        retrieved_messages = messages_from_dict(stored_memory)
        chat_history = ChatMessageHistory(messages=retrieved_messages)
    else:
        chat_history = ChatMessageHistory()
    memory = ConversationBufferMemory(memory_key="chat_history",
                                      return_messages=True,
                                      output_key='answer',
                                      chat_memory=chat_history
                                      )
    chain = ConversationalRetrievalChain.from_llm(
        llm_model,
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        chain_type="stuff",
        return_source_documents=True,
        verbose=True,
        condense_question_prompt=prompt_chat,
        return_generated_question=True,
        get_chat_history=get_chat_history,
        combine_docs_chain_kwargs={"prompt": prompt_doc}
        )
    return chain
