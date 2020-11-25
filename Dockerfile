FROM python:3.7

COPY . /app

# ADD ./settings /app/

# ADD .env /app

# ADD manage.py /app

# ADD Pipfile /app

# ADD Pipfile.lock /app

WORKDIR /app

RUN apt-get update

RUN pip install pipenv

RUN pipenv install --dev