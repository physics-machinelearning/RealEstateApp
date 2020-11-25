### 既存DBとの連携
- settings/settings.pyのDATABASESに既存DBの情報を書き込む
- python manage.py inspectdb


### DB初期化
- initdb /usr/local/var/postgres -E utf8

- postgres -D /usr/local/var/postgres
- createuser -P kuroki
- createdb suumo-db -O kurok

- pipenv run python manage.py makemigrations realestate
- pipenv run python manage.py migrate