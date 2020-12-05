import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

POSTGRES_USER = "kuroki"
POSTGRES_PASSWORD = "kuroki"
POSTGRES_HOST = "54.65.63.5"
POSTGRES_DB = "suumo-db"


def connect_db():
    conn = psycopg2.connect('postgresql://{user}:{password}@{host}/{db}'
                            .format(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                    host=POSTGRES_HOST, db=POSTGRES_DB))
    return conn


def get_from_db(query_dict):
    if 'select' in query_dict.keys() and 'table' in query_dict.keys():
        select = query_dict['select']
        table = query_dict['table']
        select = ', '.join(select)
        query = "SELECT " + select + " FROM " + table
        if 'where' in query_dict.keys():
            where = query_dict['where']
            where = ', '.join(where)
            query += " WHERE " + where
        if 'group_by' in query_dict.keys():
            group_by = query_dict['group_by']
            group_by = ', '.join(group_by)
            query += " GROUP BY " + group_by
        
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        col_name = [description[0] for description in cur.description]
        return result, col_name
    else:
        return