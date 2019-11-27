# Maana Q Knowledge Microservice Template: Python (Ariadne)

- Uses the [Ariadne GraphQL framework](https://ariadnegraphql.org/)
- Uses the [ASGI Lifespan middlware](https://pypi.org/project/asgi-lifespan/)
- Concurrency, app server, and containerization is provided by the [Uvicorn+Gunicorn Docker](https://github.com/tiangolo/uvicorn-gunicorn-docker) base image

## Build

```
pip install uvicorn gunicorn ariadne graphqlclient asgi-lifespan
```

## Containerize

Then you can build your image from the directory that has your Dockerfile, e.g:

```
docker build -t my-service ./
```

## Run Debug Locally

To run the GraphQL service locally with hot reload:

```
./start-reload.sh
```

and visit http://0.0.0.0:4000

For details, please refer to the [official documentation](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#development-live-reload).

## Run Locally (via Docker)

To run the GraphQL service locally (Via Docker):

```
docker run -it -p 4000:80 -t my-service
```

and visit http://0.0.0.0:4000

## Run Debug Locally (via Docker)

To run the GraphQL service via Docker with hot reload:

```
docker run -it -p 4000:80 -v $(pwd):/app my-service /start-reload-docker.sh
```

and visit http://0.0.0.0:4000

For details, please refer to the [official documentation](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#development-live-reload).

## Deploy

To simplify deployment to your Maana Q Kubernetes cluster, use the [CLI `mdeploy` command](https://github.com/maana-io/q-cli#mdeploy):

```
gql mdeploy
```

and follow the prompts.
