from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from fastapi import HTTPException
import pymilvus
from langchain.schema import messages_from_dict

from .utils import get_settings
from .prompts import prompt_doc, prompt_chat

def vector_database(
              collection_name,
              drop_existing_embeddings=False,
              doc_text=None):

    """
    Creates and returns a Milvus database based on the specified parameters.
    Args:
        doct_text: The document text. 
        collection_name: The name of the collection.
        drop_existing_embeddings: Whether to drop existing embeddings.
    Returns:
        The Milvus database.
        """

    embeddings = OpenAIEmbeddings(openai_api_key=get_settings().openai_api_key)
    if doc_text: # adding new data
        try: 
            vector_db = Milvus.from_documents(
                doc_text,
                embeddings,
                collection_name=collection_name,
                drop_old=drop_existing_embeddings,
                connection_args={"host": get_settings().milvus_host, "port": "19530"},
                # if we want to communicate between two dockers then instead of local 
                # host we need to use milvus-standalone
            )
        except pymilvus.exceptions.ParamError:
            raise HTTPException(status_code=400,
                                detail=f"collection_name {collection_name} already exist. Either set drop_existing_embeddings to true or change collection_name")
    else:
        vector_db = Milvus(
            embeddings,
            collection_name=collection_name,
            connection_args={"host": get_settings().milvus_host, "port": "19530"},
        )
    return vector_db


def get_chat_history(inputs):
    """
    Get human input only
    """
    inputs = [i.content for i in inputs]
    # inputs = [string for index, string in enumerate(inputs) if index % 2 == 0]
    return '\n'.join(inputs)


def db_conversation_chain(stored_memory, collection_name):

    """
    Creates and returns a ConversationalRetrievalChain based on the specified parameters.
    Args:
        stored_memory: Existing conversation.
        collection_name: The name of the collection (optional).
    Returns:
        The ConversationalRetrievalChain.
    """

    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        openai_api_key=get_settings().openai_api_key)  

    vector_db = vector_database(
        collection_name=collection_name,
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
        llm,
        retriever=vector_db.as_retriever(),
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
