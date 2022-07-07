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

def querier(query: str) -> pd.DataFrame:
      """
      Connects to the database, makes a query and returns the data as a Pandas dataframe.
      
      Args:
          query: Query string to be used for data extraction.
      Returns:
          data: Pandas dataframe.
      """
      conn=psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PSW, port=DB_PORT,connect_timeout=300)
      cursor=conn.cursor()
      
      data = sqlio.read_sql_query(query, conn)
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