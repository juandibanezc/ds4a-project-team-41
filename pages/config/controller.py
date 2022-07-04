import sqlite3
import pandas as pd

def conectarse(ruta):
    """
    Funcion usada para conectarse a la base de datos. Devuelve el cursor y el conn
    """
    conn=sqlite3.connect(ruta)
    cursor=conn.cursor()
    return cursor, conn
def query(ruta,transaccion):
    """
    Devuelve un dataframe segun la transaccion de SQL pasada en los argumentos y el conector a la db
    """
    return pd.read_sql_query(transaccion, conectarse(ruta)[1])