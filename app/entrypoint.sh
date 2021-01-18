#!/bin/sh

pipenv run python manage.py makemigrations

pipenv run python manage.py migrate

pipenv run gunicorn settings.wsgi:application -b 0.0.0.0:8000