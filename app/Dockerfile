FROM python:3.7

COPY . /app/

COPY ./entrypoint.sh /app/

WORKDIR /app

RUN pwd

RUN ls -a

RUN pip install pipenv

RUN pipenv install --dev

ENTRYPOINT ["entrypoint.sh"]