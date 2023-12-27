from langchain.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load(path, source):
    loader = OnlinePDFLoader(path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(docs)
    for doc in docs:
        doc.metadata["source"] = source
    return docs


# https://sos-ch-dk-2.exo.io/dls-bs-prod-public/28/48/36/ba267b11c0396c50bdcb779aa6/20170118_Beschlussprotokoll/original.pdf
