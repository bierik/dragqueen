import logging

import chromadb
from langchain.vectorstores.chroma import Chroma

logger = logging.getLogger("mindreader")


class Vectorstore:
    def __init__(self, host, port, collection_name, embedding_function):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection_name = collection_name
        self.embedding_function = embedding_function
        self.store = None

    def reset(self):
        logger.info("Resetting vectorstore")
        self.client.reset()
        self.store = None

    def init(self):
        if self.store:
            return
        self.store = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_function,
        )

    def add_documents(self, documents):
        if not documents:
            return
        document_count = len(documents)
        logger.info(f"Embedding {document_count} documents")
        self.store.add_documents(documents)

    def as_retriever(self, **kwargs):
        return self.store.as_retriever(**kwargs)
