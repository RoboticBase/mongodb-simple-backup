FROM python:3.7-alpine
MAINTAINER Nobuyuki Matsui <nobuyuki.matsui@gmail.com>

COPY ./app /opt/app

WORKDIR /opt/app

RUN apk update && \
    apk add --no-cache libffi-dev openssl-dev mongodb-tools && \
    apk add --no-cache --virtual .build python3-dev build-base linux-headers && \
    pip install pipenv && \
    pipenv install --system && \
    apk del --purge .build && \
    rm -r /root/.cache

RUN chmod a+x /opt/app/main.py

ENTRYPOINT /opt/app/main.py
