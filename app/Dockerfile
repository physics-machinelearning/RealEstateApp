FROM python:3.7

COPY . /app/

WORKDIR /app

RUN pwd

RUN ls -a

RUN pip install pipenv

RUN pipenv install --dev

ENTRYPOINT ["sh", "/entrypoint.sh"]