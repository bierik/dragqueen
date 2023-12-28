from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    """
Du bist ein Assistent, um Fragen mittels Kontext zu beantworten.
Benutze folgenden Kontext, um die Frage zu beantworten.
Wenn du die Antwort nicht kennst, sage einfach, dass du es nicht weist.
Verwende maximal drei Sätze und halte die Antwort kurz und prägnant.

Frage: {question}

Kontext: {context}

Antwort:
"""
)
