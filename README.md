# Production level scalable ChatBot

## About
Creating a chatBot using openAI. Here are few advantages.
* The chatBot uses a Retriever-Generator base module to reduce costs.
  * The Retriever fetches the text of concern while the Generator creates a response from the fetched content.
  * The Retriever can be replaced by any open source LLMs to reduce cost, but there is currently no such option for the Generator.
* Embeddings are created once and stored in a Milvus vector database, saving cost if the same content is fed again.
* Milvus and PostgreSQL are open source and their advantages can be read on their website.

## Prerequisite
* Install [docker engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
* Install [docker compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository)
* Install and run [milvus](https://milvus.io/docs/install_standalone-docker.md)
* Install [haystack](https://docs.haystack.deepset.ai/docs/installation) 

## Getting started
Three end points have been implemented.  
* doc_ingestion: Insert document 
* query: ask query to be responded by chat bot. 

### documnet ingestion `/doc_ingestion`
```
{
  "api_key": "string",
  "dir_path": "string"
}
```

dir_path: path of folder where your documents are present. 
Example is `./data`  
Following formats are allowed
* txt
* pdf
* docs

### query tex `/query`
```
{
  "api_key": "string",
  "text": "string",
  "session_id": string
}
```

text: query  
apikey: openai api key  
session_id: sessions are created. Each session represents new conversation and do not have memory of other sessions.

### session deletion `/delete`

user can delete session by providing seesion_id
```
{
  "session_id": str
}
```


## TODOs
- [X]  Automate working_memory ingestion 
- [ ]  Integrate PostgreSQL
- [ ]  Filter data (profanity/offensive language) at indexing
- [X]  Add validator to the input
- [ ]  Cost analysis for the openAI api usage
- [ ]  Allow OpenAI different models


