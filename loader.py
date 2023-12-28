import logging

from langchain.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger("mindreader")


class Loader:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    def extract_documents(self, path):
        logger.info(f"Extracting PDF from {path}")
        loader = OnlinePDFLoader(path)
        return loader.load()

    def split(self, documents, source):
        logger.info(f"Splitting document")
        docs = self.splitter.split_documents(documents)
        for doc in docs:
            doc.metadata["source"] = source
        return docs

    def load(self, path, source):
        documents = self.extract_documents(path)
        return self.split(documents, source)
