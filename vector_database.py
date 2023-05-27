from langchain.vectorstores import Milvus
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.chat_models import ChatOpenAI
from data import load_n_split
from utils import get_settings

from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain

from langchain.schema import messages_from_dict, messages_to_dict

llm = ChatOpenAI(model_name='gpt-3.5-turbo',openai_api_key=get_settings().openai_api_key)


def vector_db(doct_text,
              collection_name, 
              embeddings = OpenAIEmbeddings(openai_api_key=get_settings().openai_api_key)):
    return Milvus.from_documents(
        doct_text,
        embeddings,
        collection_name = collection_name,
        connection_args={"host": "127.0.0.1", "port": "19530"},
        
    )

def db_conversation_chain(retrieve_from_db, collection_name):
    docs = load_n_split('abc') #TODO Define collection name, currently its using random path that does not exisit
    retriever = vector_db(docs, collection_name=collection_name)
    
    if retrieve_from_db:
        retrieved_messages = messages_from_dict(retrieve_from_db)
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
                                            return_source_documents=True)


    return chain