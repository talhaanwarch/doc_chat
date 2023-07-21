import os
import requests

from joblib import Memory
import structlog

cache_dir = "./model_cache"
memory = Memory(cache_dir, verbose=0)
logger = structlog.getLogger()

@memory.cache
def download_model(llm_name, model_info):
    """
    Download the specified LLM model.
    Args:
        llm_name: The name of the LLM model.
        model_info: Dictionary containing the URL and file path for the model.
    Returns:
        The file path of the downloaded model.
    """
    model_url = model_info.get("url")
    model_filepath = model_info.get("filepath")

    if not os.path.isfile(model_filepath):
        logger.info(f"{llm_name} LLM downloading ... ")
        response = requests.get(model_url, stream=True)

        # Open the file in binary mode and write the contents of the response to it in chunks
        # This is a large file, so be prepared to wait.
        with open(model_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return model_filepath

@memory.cache
def download_and_load_llm_model(llm_name, model_info):
    """
    Download and load the specified LLM model.
    Args:
        llm_name: The name of the LLM model.
        model_info: Dictionary containing the URL and file path for the model.
    Returns:
        The loaded LLM model and the name of the embeddings used by the model.
    """
    model_filepath = download_model(llm_name, model_info)

    try:
        from langchain.llms import GPT4All
        llm = GPT4All(model=model_filepath,  verbose=True)
        embeddings_name = "sentence"
    except Exception as e:
        logger.error(f"Error loading {llm_name} LLM: {e}")
        llm = None
        embeddings_name = None

    return llm, embeddings_name





@memory.cache
def get_embeddings(embedding_name="all-MiniLM-L6-v2"):
    """
    Get embeddings based on the specified name.
    Args:
        embedding_name: The name of the embeddings ('all-mpnet-base-v2' by default).
    Returns:
        The embeddings object.
    """
    if embedding_name == "all-MiniLM-L6-v2":
        from langchain.embeddings.huggingface import HuggingFaceEmbeddings
        path = './llms/all-MiniLM-L6-v2'
        if os.path.isdir(path):
            logger.info(f'{embedding_name} is in llm folder')
            embeddings = HuggingFaceEmbeddings(model_name=path)  # TODO add validation to make sure it's present
            logger.info(f'{embedding_name} is in loaded')
        else:
            logger.info(f'{embedding_name} downloading ... ')
            embeddings = HuggingFaceEmbeddings(embedding_name)
        return embeddings
