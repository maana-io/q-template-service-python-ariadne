FROM tiangolo/uvicorn-gunicorn-starlette:python3.8-slim

# These are core dependencies and should be updated with care
RUN pip3 install 'uvicorn==0.11.*' 'gunicorn==20.*' 'ariadne==0.11.*' 'graphqlclient==0.2.*' 'asgi-lifespan==1.0.1' python-dotenv requests

COPY ./app /app
COPY .env /.env
COPY ./gunicorn_conf.py /
COPY requirements.txt /
COPY start.sh /start.sh
RUN chmod +x /start.sh

RUN pip3 install -r /requirements.txt

WORKDIR /
EXPOSE 4000
CMD /start.sh
