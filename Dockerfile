FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

RUN pip install ariadne uvicorn gunicorn asgi-lifespan python-dotenv requests graphqlclient

COPY ./app /app
COPY .env /.env
COPY start.sh /start.sh
WORKDIR /
