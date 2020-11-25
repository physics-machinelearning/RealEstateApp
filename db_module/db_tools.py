import os
import argparse
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base


load_dotenv()

MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_DB = os.environ['MYSQL_DB']


def dropall(table_name):
    engine = create_engine('postgresql://{user}:{password}@{host}/{db}'
                           .format(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                   host=MYSQL_HOST, db=MYSQL_DB),
                           encoding='utf-8', echo=False)
    conn = engine.connect()
    conn.execute("DROP TABLE IF EXISTS "+table_name+";")


def getall(table_name):
    conn = psycopg2.connect('postgresql://{user}:{password}@{host}/{db}'
                              .format(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                      host=MYSQL_HOST, db=MYSQL_DB))
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table_name)
    col_name = [description[0] for description in cur.description]
    all_data = []
    for each in cur:
        all_data.append(each)
    df = pd.DataFrame(all_data, columns=col_name)
    return df


def connect_db():
    engine = create_engine('postgresql://{user}:{password}@{host}/{db}'
                            .format(user=MYSQL_USER, password=MYSQL_PASSWORD,
                            host=MYSQL_HOST, db=MYSQL_DB))
    session = Session(bind = engine)
    return session


def create_table():
    engine = create_engine('postgresql://{user}:{password}@{host}/{db}'
                            .format(user=MYSQL_USER, password=MYSQL_PASSWORD,
                            host=MYSQL_HOST, db=MYSQL_DB))
    # if not engine.dialect.has_table(engine, MYSQL_DB):
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('function_name',
                        type=str,
                        help='set fuction name in this file')
    parser.add_argument('-i', '--func_args',
                        nargs='*',
                        help='args in function',
                        default=[])
    args = parser.parse_args()

    # このファイル内の関数を取得
    func_dict = {k: v for k, v in locals().items() if callable(v)}
    # 引数のうち，数値として解釈できる要素はfloatにcastする
    func_args = [float(x) if x.isnumeric() else x for x in args.func_args]
    # 関数実行
    ret = func_dict[args.function_name](*func_args)
