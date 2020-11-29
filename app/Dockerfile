FROM python:3.7

COPY . /app/

COPY ./static/ /static/

# COPY ./entrypoint.sh /app/

WORKDIR /app

# RUN chmod +x entrypoint.sh

RUN pwd

RUN ls -a

RUN pip install pipenv

RUN pipenv install --skip-lock

# ENTRYPOINT ["sh", "/entrypoint.sh"]

# CMD ["pipenv", "run", "python", "manage.py", "makemigrations", "realestate"]

# CMD ["pipenv", "run", "python", "manage.py", "migrate"]
