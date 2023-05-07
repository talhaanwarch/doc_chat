from haystack.utils import convert_files_to_docs
from haystack.nodes import PreProcessor
from utils import document_store


def read_data(dir_path):
    all_docs = convert_files_to_docs(dir_path=dir_path)
    return all_docs

def preprocess(docs):
    # Preprocess and add the documents to the document store
    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        clean_header_footer=False,
        split_by="word",
        split_length=500,
        split_respect_sentence_boundary=True,
    )
    preprocessed_docs = preprocessor.process(docs)
    return preprocessed_docs



