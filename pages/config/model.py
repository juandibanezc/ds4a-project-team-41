import sqlite3
import pandas as pd

def querier(ruta_db, query):
     conn = sqlite3.connect(ruta_db)
     c = conn.cursor()
     c.execute("SELECT * FROM sqlite_master WHERE type='table';")
     df = pd.read_sql_query(query, conn)
     conn.close()

     return df