# Maana Q Knowledge Microservice Template: Python (Ariadne)

- Containerization is done using the [Uvicorn+Gunicorn Docker](https://github.com/tiangolo/uvicorn-gunicorn-docker) base image

## Build

It is recommended to use the [Conda](https://conda.io/projects/conda/en/latest/index.html) [environment](https://conda.io/projects/conda/en/latest/user-guide/concepts/environments.html) mechanism and ensure the right mix of `python`, `pip`, and packages are installed and active:

```
conda env create -f environment.yml
conda activate maana-tensorflow
docker build -t maana-python-ariadne .
```

## Run Local (via Docker)

To run the GraphQL service locally (Via Docker):

```
docker run -it -p 4000:80 -t maana-python-ariadne
```

## Run Debug (via Docker)

To run the GraphQL service locally (Via Docker) with hot reload:

```
docker run -it -p 4000:80 -v $(pwd):/app maana-python-ariadne /start-reload.sh
```

For details, please refer to the [official documentation](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#development-live-reload).

## Deploy

```
gql mdeploy
```

## Internals

To create an environment file:

```
conda env export > environment.yml
```
