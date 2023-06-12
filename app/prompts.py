from langchain.prompts import PromptTemplate

prompt_template_doc = """You are an AI assitant named as TAC. Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""
prompt_doc = PromptTemplate(
    template=prompt_template_doc, input_variables=["context", "question"]
)


prompt_template_chat = """You are an AI assitant named as TAC. Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""


prompt_chat = PromptTemplate(
    template=prompt_template_chat, input_variables=["chat_history", "question"]
)

