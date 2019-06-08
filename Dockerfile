FROM python:3.7-stretch
MAINTAINER Nobuyuki Matsui <nobuyuki.matsui@gmail.com>

COPY ./app /opt/app

WORKDIR /opt/app

RUN apt update && apt upgrade -y && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4 && \
    echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" >> /etc/apt/sources.list.d/mongodb-org-4.0.list && \
    apt update && \
    apt install mongodb-org-tools -y && \
    pip install pipenv && \
    pipenv install --system

RUN chmod a+x /opt/app/main.py

ENTRYPOINT /opt/app/main.py
