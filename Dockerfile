FROM python:3.10-alpine

RUN apk add cmake

RUN pip install poetry==1.3.2

RUN mkdir -m 777 /app

WORKDIR /app/

COPY . .

RUN poetry install --no-root

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
