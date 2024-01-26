#!/usr/bin/env python3
import logging
import os
import sys

import click
from dotenv import load_dotenv
from dragqueen.loader import Loader
from dragqueen.scrapper import Scrapper
from dragqueen.vectorstore import Vectorstore
from langchain.embeddings import HuggingFaceEmbeddings

load_dotenv()


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


scrapper = Scrapper("https://dls.staatsarchiv.bs.ch")
paginator = scrapper.paginate()

vectorstore = Vectorstore(
    os.getenv("CHROMA_HOST", "chroma"),
    os.getenv("CHROMA_PORT", "8000"),
    "dls_rag_collection",
    HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2"),
)
vectorstore.init()

loader = Loader()


@click.group()
def main():
    pass


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
