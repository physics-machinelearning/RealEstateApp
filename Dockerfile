FROM python:3.7

COPY . /app

# psycopg2のインストール
# RUN apt update \
#     && apt install gcc python3-dev musl-dev \
#     && apt install postgresql-dev \
#     && pip install psycopg2 \

WORKDIR /app

RUN pip install pipenv

RUN pipenv install --dev