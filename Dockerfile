#FROM python:3.10-alpine
FROM debian:bookworm

RUN apt update

RUN apt install python3 python3-pip -y

RUN python3 -m pip install --break-system-packages poetry==1.3.2

RUN mkdir -m 777 /app

WORKDIR /app/

COPY ./src/ .

RUN poetry install --no-root

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
