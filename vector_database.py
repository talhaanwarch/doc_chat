from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from data import load_n_split
from utils import get_settings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os
from langchain.schema import messages_from_dict
from langchain.llms import GPT4All, LlamaCpp
from utils import get_settings
from fastapi import HTTPException

import pymilvus

def vector_db(doct_text,
              collection_name,
              drop_existing_embeddings=False,
              embeddings_name='sentence'):
    
    """
    Creates and returns a Milvus database based on the specified parameters.
    Args:
        doct_text: The document text.
        collection_name: The name of the collection.
        drop_existing_embeddings: Whether to drop existing embeddings.
        embeddings_name: The name of the embeddings ('openai' or 'sentence').
    Returns:
        The Milvus database.
        """
    
    if embeddings_name == 'openai':
        embeddings = OpenAIEmbeddings(openai_api_key=get_settings().openai_api_key)
    elif embeddings_name == 'sentence':
        embeddings = HuggingFaceEmbeddings()
    else:
        print('invalid embeddings')
    try: 
        db = Milvus.from_documents(
            doct_text,
            embeddings,
            collection_name=collection_name,
            drop_old=drop_existing_embeddings,
            connection_args={"host": "127.0.0.1", "port": "19530"},
            
        )
    except pymilvus.exceptions.ParamError:
        raise HTTPException(status_code=400,
                            detail=f'collection_name {collection_name} already exist. Either set drop_existing_embeddings to true or change collection_name')

    return db


def db_conversation_chain(llm_name, stored_memory, collection_name):

    """
    Creates and returns a ConversationalRetrievalChain based on the specified parameters.
    Args:
        llm_name: The name of the language model ('openai', 'gpt4all', or 'llamacpp').
        stored_memory: Existing conversation.
        collection_name: The name of the collection (optional).
    Returns:
        The ConversationalRetrievalChain.
    """

    if llm_name == 'openai':
        llm = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=get_settings().openai_api_key)
    elif llm_name == 'gpt4all':
        llm = GPT4All(model='llms/ggml-gpt4all-j.bin', n_ctx=1000, verbose=True)
    elif llm_name == 'llamacpp':
        llm = GPT4All(model='llms/ggml-gpt4all-l13b-snoozy.bin', n_ctx=1000, verbose=True)
    docs = load_n_split('abc') #TODO Define collection name, currently its using random path that does not exisit
    retriever = vector_db(docs, collection_name=collection_name)
   
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
    chain = ConversationalRetrievalChain.from_llm(llm,
                                                    retriever=retriever.as_retriever(),
                                                    memory=memory,
                                                    chain_type="stuff",
                                                    return_source_documents=True,
                                                    verbose=True)

    return chain