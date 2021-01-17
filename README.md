## 概要
東京23区の賃貸物件検索サイトから情報をパースし、賃貸価格の予測モデルを作成、実際の額と予測額との差額から、お得な物件をお勧めするwebアプリ

## EC2上での実行方法
### docker install
- sudo yum update
- sudo yum install -y docker
- sudo service docker start

- sudo usermod -a -G docker ec2-user
- cat /etc/group |grep docker

一旦ログアウト
- docker info

### install docker-compose
- sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
- sudo chmod +x /usr/local/bin/docker-compose
- docker-compose --version

### install git
- yum install git

### 実行
- docker-compose up -d

## Localでの実行メモ
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
