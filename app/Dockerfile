FROM python:3.7

COPY . /app/

COPY ./entrypoint.sh /app/

WORKDIR /app

RUN chmod +x entrypoint.sh

RUN pwd

RUN ls -a

RUN pip install pipenv

RUN pipenv install --skip-lock

ENTRYPOINT ["sh", "/entrypoint.sh"]