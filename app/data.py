from typing import List, Optional
from langchain.docstore.document import Document
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import TokenTextSplitter
import requests
import tempfile

class CleanTextLoader(TextLoader):
    """Load text files."""

    def __init__(self, file_path: str, encoding: Optional[str] = None):
        """Initialize with file path."""
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> List[Document]:
        """Load from file path."""
        with open(self.file_path, encoding=self.encoding) as f:
            text = f.read()
        text = self.clean_text(text)
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]

    def clean_text(self, text):
        # remove leading and trailing whitespace from each line
        lines = (line.strip() for line in text.splitlines())
        # replace two or more whitespace characters with a single space
        text = ' '.join(line for line in lines)
        text = ' '.join(text.split())
        # remove two or more consecutive empty lines
        text = '\n'.join(line for line in text.splitlines() if line.strip())
        return text


class TextProcessor:
    def __init__(self, urls: list[str], text_splitter: Optional[str] = "token"):
        self.text_splitter = text_splitter
        self.urls = urls

    def download_text_files(self, urls):
        """
        Download files in a temp directory.
        Then read the file using langchain loader. 
        By simply changing the loader we can load different types of files
        """
        docs = []
        for url in urls:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                with tempfile.TemporaryDirectory() as temp_dir:
                    file_path = f"{temp_dir}/{url.split('/')[-1]}"
                    with open(file_path, "w") as f:
                        f.write(response.text)
                    loader = CleanTextLoader(file_path)
                    docs.append(loader.load()[0])
        return docs

    def load_n_split(self):
        """
        path: directory path having text files.
        This function reads text files, cleans them, and then splits them into chunks.
        """
        documents = self.download_text_files(self.urls)
        if self.text_splitter == "token":
            text_splitter = TokenTextSplitter(chunk_size=80, chunk_overlap=20)
        else:
            print('Invalid splitter')
        doc_text = text_splitter.split_documents(documents)
        return doc_text
    