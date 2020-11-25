## PostgreSQL
### 環境構築
- postgres -D /usr/local/var/postgres
- createuser -P kuroki
- createdb suumo-db -O kurok
jupyter notebookのカーネル作成
- pipenv run python -m ipykernel install --user --name="kernel name"

## sqlalchemy
### migration初期設定
- mkdir db
- cd db
- migrate create migrate "archive"
- cd migrate
- pipenv run python manage.py version_control postgresql://ID:pass@host/db .
### migration実行
- pipenv run python manage.py script "message"
- "message".pyを書き換え
- pipenv run python manage.py test
- pipenv run python manage.py upgrade
- pipenv run python manage.py downgrade version (version指定)
参考：https://qiita.com/t2kojima/items/5c7f9978f98b1a897d73
### 使い方
全削除
- pipenv run python db_tools.py dropall -i table名

## 地理情報
### 国交省
- https://qiita.com/laqiiz/items/842fe2a32e80bac92364