FROM python:3.7

COPY . /app

# psycopg2のインストール
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

WORKDIR /app

RUN apt-get update

RUN pip install pipenv

RUN pipenv install --dev　--skip-lock