FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

RUN apt-get update && apt-get install python3.11 python3-pip -y

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi --only main

COPY dragqueen /app/dragqueen
COPY cli.py /app/

CMD exec uvicorn dragqueen.server:app --host 0.0.0.0 --port 8000
