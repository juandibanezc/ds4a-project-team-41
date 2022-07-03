from plotly.graph_objs._figure import Figure
import plotly.express as px
#from pages.config.model import querier
from datetime import datetime
import geopandas as gpd
from typing import Tuple
import pandas as pd
import locale

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

# Set date names to spanish
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def report_graph_4(date_filter: list) -> Tuple[str,str]:

  q = f"""
      SELECT 
        CASE  
          WHEN glb_comunas_corregimientos.descripcion LIKE 'Corregimiento%' THEN 'Rural'
          ELSE glb_comunas_corregimientos.descripcion
        END as comuna, 
        COUNT(DISTINCT Modulo_PQR_Sector_Salud.id) as cantidad 
      FROM 
        Modulo_PQR_Sector_Salud 
        JOIN glb_barrios_veredas ON CAST(Modulo_PQR_Sector_Salud.glb_barrio_vereda_id AS varchar) = CAST(glb_barrios_veredas.id AS varchar) 
        JOIN glb_comunas_corregimientos ON CAST(glb_barrios_veredas.glb_comunas_corregimiento_id AS varchar) = CAST(glb_comunas_corregimientos.id AS varchar) 
        JOIN tipo_peticion ON CAST(Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_id AS varchar) = CAST(tipo_peticion.ID AS varchar)
      WHERE 
        to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'
      GROUP BY 
        comuna
      """

  df = querier(q)
  df.index = df['comuna']
  comuna_list = ['Comuna 1', 'Comuna 2', 'Comuna 3', 'Comuna 4', 'Comuna 5', 'Comuna 6','Comuna 7', 'Comuna 8', 'Comuna 9', 'Comuna 10', 'Comuna 11', 'Comuna 12', 'Comuna 13', 'Rural', 'Sin Informacion']
  comuna_list = [c for c in comuna_list if c in df['comuna'].unique()]
  df = df.loc[comuna_list].reset_index(drop=True)
  
  # Creating plotly bar chart using the pre-processed data
  fig = px.bar(df, x="comuna", y="cantidad", orientation='v',
      labels={"comuna": "Comuna",
              "cantidad": "Cantidad de PQRS"}
  )
  fig.update_traces(texttemplate='%{y:.2s}', textposition='outside')
  fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
  fig.update_layout(
                      plot_bgcolor='#fff',
                      uniformtext_minsize=8, uniformtext_mode='hide',
                      font={
                          'family': 'Rubik, sans-serif',
                          'color': '#515365'
                      },
                      title='Distribución de PQRS radicadas en la secretaria <br> de salud municipal de Ibagué - Dirección <br> de aseguramiento según comuna',
                      title_x=0.5,
                      title_font_family='Rubik, sans-serif',
                      title_font_size=15
                      )
  fig.write_image("assets/images/report_graph_4.svg")

  # Text section
  date = datetime.strptime(date_filter[1], '%Y-%m-%d').date()
  year = date.strftime("%Y")
  month_name = (date.strftime("%B"))
  df_comunas = df[df['comuna'].str.startswith('Comuna')].sort_values(by='cantidad', ascending=False).reset_index(drop=True)
  df_tail = df_comunas.tail(2).reset_index(drop=True)
  
  text1 = f"""
  Se realiza la caracterización de la población que según la radicación de PQRS del mes de {month_name.upper()} {year} se le han vulnerado sus derechos o sus requerimientos en salud, con esto podemos identificar qué comuna requiere apoyo.
  """
  
  text2 = f"""
  Durante el mes de {month_name.upper()} {year} se radicaron un total de {df['cantidad'].sum()} PQRS, de los cuales el {round((df_comunas.loc[0,'cantidad']/df['cantidad'].sum())*100,2)}% corresponde a la {df_comunas.loc[0,'comuna'].lower()}, {round((df_comunas.loc[1,'cantidad']/df['cantidad'].sum())*100,2)}% corresponde a la {df_comunas.loc[1,'comuna'].lower()}, {round((df_comunas.loc[2,'cantidad']/df['cantidad'].sum())*100,2)}% corresponden a la {df_comunas.loc[2,'comuna'].lower()} de Ibagué, donde los habitantes de estas comunas fueron los que más radicaron PQRS en busca del cumplimiento de sus derechos en salud.
  En este periodo de tiempo la {df_tail.loc[0,'comuna'].lower()} y la {df_tail.loc[1,'comuna'].lower()} de Ibagué presentaron el nivel más bajo de PQRS radicados en la Dirección de Aseguramiento de la Secretaria de Salud Municipal de Ibagué ya que no realizó la radicación de ninguna queja, reclamo o sugerencia.
  El {(df.loc[df['comuna']=='Sin Informacion','cantidad'].values[0]/df['cantidad'].sum())*100}% de PQRS radicados no cuentan con la información para ser tabulados, ya que no se encuentran identificados, diligenciados los datos o fueron radicados por entidades públicas o privadas las cuales no aplican en esta clasificación.
  """

  return text1, text2

tx1, tx2 = report_graph_4(['2022-01-01','2022-01-31'])
print(tx1)
print(tx2)
  