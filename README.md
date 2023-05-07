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
Two end points have been implemented.  
* doc_ingestion: Insert document 
* query: ask query to be responded by chat bot. 

### doc_ingestion
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

### query
```
{
  "api_key": "string",
  "text": "string",
  "working_memory": [
    "string"
  ]
}
```

text: query  
apikey: openai api key  
working_memory: a list of strings, responded by chatbot. In beginning this should be empty.
Once user got the working_memory, send it back to the api.


## TODOs
- [ ]  Automate working_memory ingestion 
- [ ]  Integrate PostgreSQL
- [ ]  Filter data (profanity/offensive language) at indexing
- [ ]  Add validator the input
- [ ]  Cost analysis for the openAI api usage
- [ ]  Allow OpenAI different models


