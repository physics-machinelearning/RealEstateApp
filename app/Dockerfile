FROM python:3.7

COPY ./app app

WORKDIR /app

RUN pip install pipenv

RUN pipenv install --dev

RUN pipenv graph

ENTRYPOINT ["sh", "/entrypoint.sh"]