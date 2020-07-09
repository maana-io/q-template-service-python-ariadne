# Maana Q Knowledge Microservice Template: Python (Ariadne)

- Uses the [Ariadne GraphQL framework](https://ariadnegraphql.org/)
- Uses the [ASGI Lifespan middlware](https://pypi.org/project/asgi-lifespan/)
- Concurrency, app server, and containerization is provided by the [Uvicorn+Gunicorn Docker](https://github.com/tiangolo/uvicorn-gunicorn-docker) base image

## Features

### Maana Q Client (i.e., peer-to-peer)

It is possible, though not generally preferred, for services to depend directly on other services, passing requests through a secure CKG endpoint.  This template includes the necessary authentication code for your convenience.  Simply supply environment settings and use the `client` from the GraphQL context:

```bash
#
# ---------------APPLICATION VARIABLES-------------------
#

MAANA_ENDPOINT_URL=
```

Authentication settings are defined in `.auth.env` - this file should not committed to version control to avoid leaking access keys.

```bash

#
# ---------------AUTHENTICATION VARIABLES--------------------
#

# keycloak or auth0
AUTH_PROVIDER=

# URL for auth server (without path), i.e. https://keycloakdev.knowledge.maana.io:8443
AUTH_DOMAIN=

# Keycloak or auth0 client name/id.
AUTH_CLIENT_ID=

# Client secret for client credentials grant
AUTH_SECRET=

# Auth audience for JWT
# Set to same value as REACT_APP_PORTAL_AUTH_IDENTIFIER in Maana Q deployment ENVs)
# NOTE: For use of keycloak in this app, this value should match both the realm and audience values. 
AUTH_IDENTIFIER=
```

And, in your resolver:

```python
    # A resolver can access the graphql client via the context.
    client = info.context["client"]

    # Query all maana services.
    result = client.execute('''
    {
        allServices {
            id
            name
        }
    }
    ''')

    print(result)
```

### Other GraphQL clients

You can create GraphQL clients to talk to other services, with or without authentication, with the same or different authentication settings

```python
from app.qclient import QClient

# CKG service URL, use same authentication as Q settings above
client = QClient('https://<q url>/service/<ckgserviceid>/graphql')

# GraphQL service without authentication
client = QClient('https://some-other-service-url/', require_auth=False)

# GraphQL service with different authentication
client = QClient('https://authenticated-service/', auth_provider='keycloak', auth_domain=..., auth_client_id=..., auth_secret=..., auth_identifier=...)
```

## Build

This template requires Python 3 to run.

```
pip3 install 'uvicorn==0.11.*' 'gunicorn==20.*.*' 'ariadne==0.11.*' 'graphqlclient==0.2.*' 'asgi-lifespan==1.0.1' python-dotenv requests
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
docker run -it -p 4000:4000 -t my-service
```

and visit http://0.0.0.0:4000

## Run Debug Locally (via Docker)

To run the GraphQL service via Docker with hot reload:

```
docker run -it -p 4000:4000 -v $(pwd):/app my-service /start-reload-docker.sh
```

and visit http://0.0.0.0:4000

For details, please refer to the [official documentation](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#development-live-reload).

## Editing

To update any changes made to the service you will need to re run docker build.

To add new dependencies it is advised to add them to `requirements.txt` instead of modifying Dockerfile directly,
as this will significantly speed up build process due to docker layer caching.

## Deploy

To simplify deployment to your Maana Q Kubernetes cluster, use the [CLI `mdeploy` command](https://github.com/maana-io/q-cli#mdeploy):

```
gql mdeploy
```

and follow the prompts.
