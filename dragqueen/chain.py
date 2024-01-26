from operator import itemgetter

from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(prompt, llm, retriever):
    rag_chain_from_docs = (
        {
            "context": lambda input: format_docs(input["documents"]),
            "question": itemgetter("question"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return RunnableParallel(
        {"documents": retriever, "question": RunnablePassthrough()}
    ) | {
        "documents": lambda input: [doc.metadata for doc in input["documents"]],
        "answer": rag_chain_from_docs,
    }
