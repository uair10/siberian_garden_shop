FROM python:3.11-slim-buster as python-base

RUN apt-get update \
    && apt-get install -y gcc libpq-dev

FROM python-base as production
WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY seeds_shop /usr/src/app/seeds_shop
