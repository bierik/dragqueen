import uuid
from operator import itemgetter
from pathlib import Path

import chromadb
from chromadb.config import Settings
from langchain.chat_models import ChatOllama
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, S3FileLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

loader = PyPDFLoader(str(Path(__file__).parent / "fixtures" / "sample2.pdf"))
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

embeddings = OllamaEmbeddings(base_url="http://gpu01t.4teamwork.ch:80", model="llama2")

chroma_client = client = chromadb.HttpClient(settings=Settings(allow_reset=True))


class EmbeddingFunction:
    def __call__(self, input):
        return embeddings.embed_documents(input)


chroma_client.reset()
collection = client.create_collection(
    name="my_collection", embedding_function=EmbeddingFunction()
)

for chunk in chunks:
    collection.add(
        ids=[str(uuid.uuid1())],
        metadatas=chunk.metadata,
        documents=chunk.page_content,
    )


vectorstore = Chroma(
    client=client,
    collection_name="my_collection",
    embedding_function=embeddings,
)
retriever = vectorstore.as_retriever()

llm = ChatOllama(base_url="http://gpu01t.4teamwork.ch:80", model="llama2")

prompt = PromptTemplate.from_template(
    """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.

Question: {question}

Context: {context}

Answer:
"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain_from_docs = (
    {
        "context": lambda input: format_docs(input["documents"]),
        "question": itemgetter("question"),
    }
    | prompt
    | llm
    | StrOutputParser()
)
rag_chain_with_source = RunnableParallel(
    {"documents": retriever, "question": RunnablePassthrough()}
) | {
    "documents": lambda input: [doc.metadata for doc in input["documents"]],
    "answer": rag_chain_from_docs,
}

print(rag_chain_with_source.invoke("How are neutrinos produced?"))
