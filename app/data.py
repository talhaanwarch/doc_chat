import boto3
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders import PyPDFLoader
from typing import List, Optional
from langchain.text_splitter import TokenTextSplitter
import tempfile
import os

from .utils import get_settings


class S3FileLoader(BaseLoader):
    """Loading logic for loading documents from S3."""

    def __init__(self,
                aws_access_key_id: Optional[str] = get_settings().aws_access_key_id,
                aws_secret_access_key: Optional[str] = get_settings().aws_secret_access_key,
                region_name: Optional[str] = get_settings().region_name):
        """Initialize with credentials."""
        self.s3 = boto3.client(service_name='s3',
                      region_name=region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)


    def parse_s3_uri(self, s3_uri):
        # Remove the "s3://" prefix from the URI
        s3_uri = s3_uri.replace("s3://", "")

        # Split the URI into bucket and key components
        bucket, key = s3_uri.split("/", 1)

        return bucket, key

    def load(self, s3_uris: List[str]) -> List[Document]:
      
        all_documents = []
        for s3_uri in s3_uris:
            bucket, key = self.parse_s3_uri(s3_uri)
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = f"{temp_dir}/{key}"
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                self.s3.download_file(bucket, key, file_path)
                loader = PyPDFLoader(file_path)
                documents = loader.load()
                all_documents.extend(documents)

        return all_documents

    def load_and_split(self, s3_uris: List[str]) -> List[str]:
        documents = self.load(s3_uris)
        text_splitter = TokenTextSplitter(chunk_size=200, chunk_overlap=20) 
        # TODO different model has different content length
        document_texts = text_splitter.split_documents(documents)
        return document_texts





