import psycopg2
import pandas.io.sql as sqlio
import pandas as pd
import sqlite3
import re

def querier(transaccion):
     conn=psycopg2.connect(dbname='ibague-test', user='team41admin@dsfa', host='dsfa.postgres.database.azure.com', password='Proyectofinal13', port='5432',connect_timeout=300)
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