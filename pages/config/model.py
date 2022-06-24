import psycopg2
import pandas.io.sql as sqlio
import pandas as pd

def querier(transaccion):
     conn=psycopg2.connect(dbname='ibague-test', user='team41admin@dsfa', host='dsfa.postgres.database.azure.com', password='Proyectofinal13', port='5432',connect_timeout=300)
     cursor=conn.cursor()
     
     data = sqlio.read_sql_query(transaccion, conn)





     conn.close()

     return data