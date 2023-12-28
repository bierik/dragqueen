#!/usr/bin/env python3
import logging
import os
import sys
from operator import itemgetter

import click
from dotenv import load_dotenv
from langchain.chat_models import ChatOllama
from langchain.embeddings import OllamaEmbeddings
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from loader import Loader
from prompt import prompt
from scrapper import Scrapper
from vectorstore import Vectorstore

load_dotenv()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("mindreader")

scrapper = Scrapper("https://dls.staatsarchiv.bs.ch")
paginator = scrapper.paginate()

vectorstore = Vectorstore(
    os.getenv("CHROMA_HOST", "localhost"),
    os.getenv("CHROMA_PORT", "9000"),
    "dls_rag_collection",
    OllamaEmbeddings(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://gpu01t.4teamwork.ch:80"),
        model="llama2",
    ),
)
vectorstore.init()
retriever = vectorstore.as_retriever()

loader = Loader()

llm = ChatOllama(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://gpu01t.4teamwork.ch:80"),
    model="llama2",
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


@click.group()
def main():
    pass


@main.command()
@click.argument("question")
def ask(question):
    vectorstore.init()
    return rag_chain_with_source.invoke(question)


@main.command()
def load():
    vectorstore.init()
    for file in paginator:
        documents = loader.load(file["s3_path"], file["identifier"])
        vectorstore.add_documents(documents)


@main.command()
def reset():
    vectorstore.reset()


if __name__ == "__main__":
    main()
