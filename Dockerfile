FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

RUN pip install ariadne

COPY ./app /app