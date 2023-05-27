# Production level scalable ChatBot

## About
Creating a chatBot using openAI. Here are few advantages.
* The chatBot uses a Retriever-Generator base module to reduce costs.
  * The Retriever fetches the text of concern while the Generator creates a response from the fetched content.
  * Any LLM model can be used but we are using gpt3.5 turbo.
* Embeddings are created  and stored in a Milvus vector database.
* History is stored in SQLite

## Prerequisite
* Install [docker engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
* Install [docker compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository)
* Install and run [milvus](https://milvus.io/docs/install_standalone-docker.md)
* Install [langchain](https://python.langchain.com/en/latest/index.html) / [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/)

# API Documentation

This documentation provides information about the API endpoints available in the FastAPI-based API.

## Models

### DocModel

Represents the model for adding documents for ingestion.

| Field             | Type              | Description                                   |
| ----------------- | ----------------- | --------------------------------------------- |
| dir_path          | str               | The directory path of the documents to ingest. |
| collection_name   | Optional[str]     | The name of the collection (default: 'LangChainCollection'). |

### QueryModel

Represents the model for processing user queries.

| Field             | Type              | Description                                   |
| ----------------- | ----------------- | --------------------------------------------- |
| text              | str               | The user's query text.                        |
| session_id        | uuid4               | The session ID for tracking the conversation.  |
| collection_name   | Optional[str]     | The name of the collection (default: 'LangChainCollection'). |

### DeleteSession

Represents the model for deleting a session from the database.

| Field             | Type              | Description                                   |
| ----------------- | ----------------- | --------------------------------------------- |
| session_id        | uuid4               | The session ID to delete.                     |

## Endpoints

### `POST /doc_ingestion`

Endpoint to add documents for ingestion.

#### Request

- Body Parameters:
  - `doc` (DocModel): The document ingestion details.

#### Response

- Status Code: 200 (OK)
- Body: `{"message": "Documents added successfully"}`

### `POST /query`

Endpoint to process user queries.

#### Request

- Body Parameters:
  - `query` (QueryModel): The user query details.

#### Response

- Body: `{"answer": str, "cost": dict}`

### `POST /delete`

Endpoint to delete a session from the database.

#### Request

- Body Parameters:
  - `session` (DeleteSession): The session deletion details.

#### Response

- Body: The response message indicating the success or failure of the deletion operation.

## Example Usage

### Adding Documents for Ingestion

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{
    "dir_path": "/path/to/documents"
}' http://localhost:8000/doc_ingestion
```

### Processing User Queries

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{
    "text": "User query",
    "session_id": "9c17659b-f3f6-45c5-8590-1a349102512b"
}' http://localhost:8000/query
```

### Deleting a Session

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{
    "session_id": "9c17659b-f3f6-45c5-8590-1a349102512b"
}' http://localhost:8000/delete
```

