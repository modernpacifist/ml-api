FROM python:3.10-alpine

RUN pip install poetry==1.7

RUN mkdir -m 777 /app

WORKDIR /app/

COPY . .

RUN poetry --no-root install

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
