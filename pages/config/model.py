import psycopg2
import pandas.io.sql as sqlio
import pandas as pd
import sqlite3
import re
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_PSW = os.getenv('DB_PSW')
DB_PORT = os.getenv('DB_PORT')

def querier(transaccion):
     conn=psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PSW, port=DB_PORT,connect_timeout=300)
     cursor=conn.cursor()
     
     data = sqlio.read_sql_query(transaccion, conn)
     conn.close()

     return data

pattern = re.compile('([a-z]+)(\d*)', re.I)
def split_index(idx):
    m = pattern.match(idx)
    if m:
        letters = m.group(1)
        numbers = m.group(2)
        if numbers:
            return (letters, int(numbers))
        else:
            return (letters, 0)

# def querierOld(ruta_db, query):
#      conn = sqlite3.connect(ruta_db)
#      c = conn.cursor()
#      c.execute("SELECT * FROM sqlite_master WHERE type='table';")
#      df = pd.read_sql_query(query, conn)
#      conn.close()

#      return df