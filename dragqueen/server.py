#!/usr/bin/env python3
import os

from dotenv import load_dotenv
from dragqueen.chain import build_rag_chain
from dragqueen.prompt import prompt
from dragqueen.vectorstore import Vectorstore
from fastapi import FastAPI
from langchain.chat_models import ChatOllama
from langchain.embeddings import HuggingFaceEmbeddings
from langserve import add_routes

load_dotenv()

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

vectorstore = Vectorstore(
    os.getenv("CHROMA_HOST", "localhost"),
    os.getenv("CHROMA_PORT", "9000"),
    "dls_rag_collection",
    HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2"),
)
vectorstore.init()

llm = ChatOllama(
    base_url=os.getenv("OLLAMA_BASE_URL", "http://gpu01t.4teamwork.ch:80"),
    model=os.getenv("OLLAMA_MODEL", "llama2"),
)


add_routes(
    app,
    build_rag_chain(prompt, llm, vectorstore.as_retriever()),
    path="/ask",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=9900)
