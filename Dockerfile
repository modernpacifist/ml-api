FROM python:3.10-alpine

RUN apk update

RUN apk add cmake build-base

RUN pip install poetry==1.7

RUN mkdir -m 777 /app

WORKDIR /app/

COPY ./src/ .

RUN poetry install --no-root

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
