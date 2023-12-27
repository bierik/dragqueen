import uuid

import chromadb
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma

embeddings = OllamaEmbeddings(base_url="http://gpu01t.4teamwork.ch:80", model="llama2")

chroma_client = client = chromadb.HttpClient()


class EmbeddingFunction:
    def __call__(self, input):
        return embeddings.embed_documents(input)


collection = client.get_or_create_collection(
    name="my_collection", embedding_function=EmbeddingFunction()
)

vectorstore = Chroma(
    client=client,
    collection_name="my_collection",
    embedding_function=embeddings,
)


def add(document):
    collection.add(
        ids=[str(uuid.uuid1())],
        metadatas=document.metadata,
        documents=document.page_content,
    )


def reset():
    chroma_client.reset()


retriever = vectorstore.as_retriever()
