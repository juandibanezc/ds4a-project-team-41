import psycopg2
import pandas.io.sql as sqlio
import pandas as pd
import sqlite3
import re
import os
from dotenv import load_dotenv
import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_PSW = os.getenv('DB_PSW')
DB_PORT = os.getenv('DB_PORT')

print(DB_NAME)
print(DB_PSW)

def agregar_resultados_regresor(data_frame):
    """Esta funcion recibe un data frame con columnas (glb_dependencia_id VARCHAR(300), pqr_tipo_derechos VARCHAR(300), ase_tipo_poblacion_id VARCHAR(300),
                                pqr_tipo_solicitud_especifica_id VARCHAR (300), fecha_vencimiento DATE, fecha_radicacion DATE,
                                fecha_respuesta DATE)
        y realiza el cargue de los datos en la tabla resultados_modelo.
    """
    conn=psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PSW, port=DB_PORT,connect_timeout=300)
    cursor=conn.cursor()
    columnas=data_frame.columns#lista con columnas de data frame
    transaccion_1="""INSERT INTO resultados_modelo
    (glb_dependencia_id, pqr_tipo_derechos, ase_tipo_poblacion_id, pqr_tipo_solicitud_especifica_id, fecha_vencimiento, fecha_radicacion, fecha_respuesta, resultados) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    for i in range(len(data_frame)):
        serie=data_frame.iloc[i,:]
        print(serie)
        datos=[serie[element] for element in columnas]
        print(datos)
        cursor.execute(transaccion_1,datos)
        conn.commit()
    conn.close()
def agregar_resultados_clasificador(asunto, resultado):
    conn=psycopg2.connect(dbname='ibague-test', user='team41admin@dsfa', host='dsfa.postgres.database.azure.com', password='Proyectofinal13', port='5432',connect_timeout=300)
    cursor=conn.cursor()
    transaccion_1="""INSERT INTO resultados_2
    (asunto, resultado) VALUES (%s, %s)"""
    cursor.execute(transaccion_1,[asunto,resultado])
    conn.commit()
    conn.close()



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