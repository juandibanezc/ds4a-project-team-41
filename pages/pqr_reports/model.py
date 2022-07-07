from lib2to3.pgen2.pgen import DFAState
from plotly.graph_objs._figure import Figure
import plotly.express as px
from pages.config.model import querier
from datetime import datetime
import geopandas as gpd
from typing import Tuple
import pandas as pd
import locale
import sys, os

# Set date names to spanish
#locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def report_2(date_filter: list) -> Tuple[str,str]:

  q = f"""
              SELECT 
                ID AS id,
                to_char(to_date(FECHA_NACIMIENTO, 'dd/mm/yyyy'), 'yyyy-mm-dd') as fecha_nacimiento
              FROM 
                AMISALUD_TM_MAESTRO_AFILIADOS
              """

  df = querier(q)
  date = datetime.strptime(date_filter[1], '%Y-%m-%d').date()
  year = date.strftime("%Y")
  month_name = (date.strftime("%B"))
  # Transforming date of birth column to datetime and classifying each age in a category
  df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'])
  df['edad'] = (datetime.now() - df['fecha_nacimiento']).dt.days/365.25
  for i in range(len(df)):
    if df.loc[i,'edad'] <= 11:
      df.loc[i,'edad_str'] = "INFANTES MENORES DE 11 AÑOS"
    elif (df.loc[i,'edad'] >= 12) & (df.loc[i,'edad'] <= 18):
      df.loc[i,'edad_str'] = "ADOLESCENTE (12 A 18 AÑOS)"
    elif (df.loc[i,'edad'] >= 19) & (df.loc[i,'edad'] <= 26):
      df.loc[i,'edad_str'] = "JOVEN (19-26 AÑOS)"
    elif (df.loc[i,'edad'] >= 27) & (df.loc[i,'edad'] <= 59):
      df.loc[i,'edad_str'] = "ADULTOS (27 A 59 AÑOS)"
    elif df.loc[i,'edad'] > 59:
      df.loc[i,'edad_str'] = "ADULTO MAYOR (MÁS DE 59 AÑOS)"
    else:
      df.loc[i,'edad_str'] = "SIN INFORMACIÓN"

  # Grouping  the data by age category
  df_g = df.groupby(['edad_str']).agg(cantidad=('id', 'count'))
  df_g = df_g.sort_values(by='cantidad',ascending=False).reset_index(drop=False)

  # Creating plotly funnel chart using the pre-processed data
  fig = px.funnel(df_g, x='cantidad', y='edad_str', labels={'cantidad':'Cantidad','edad_str':'Edad'})
  fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
  fig.update_layout(
                      plot_bgcolor='#fff',
                      font={
                          'family': 'Rubik, sans-serif',
                          'color': '#515365'
                      },
                      title=f'Distribución de PQRS radicadas en secretaria de salud <br> municipal de Ibague - Dirección de Aseguramiento  <br> según curso de vida durante el mes de {month_name} de {year}',
                      title_x=0.5,
                      title_font_family='Rubik, sans-serif',
                      title_font_size=15
                      )
  fig.write_image("assets/images/report_2.svg")

  # Text section
  text1 = f"""
  Se realiza la caracterización de la población que según la radicación de PQRS se le han vulnerado sus derechos en salud, con el fin de identificar qué grupo etario es más vulnerable.
  """

  text2 = f"""
  Durante el mes de {month_name.upper()} de {year}, se radicaron un total de {df_g['cantidad'].sum()} PQRS, de los cuales los grupos poblacionales con mayor vulneración de sus derechos en salud fueron los {df_g.loc[0,'edad_str'].lower()} con un {round((df_g.loc[0,'cantidad']/df_g['cantidad'].sum())*100,2)}% y los {df_g.loc[1,'edad_str'].lower()} con un porcentaje de {round((df_g.loc[1,'cantidad']/df_g['cantidad'].sum())*100,2)}%.

  El {round((df_g.loc[df_g['edad_str']=='SIN INFORMACIÓN','cantidad'].values[0]/df_g['cantidad'].sum())*100,2)}% de la información no se puede cuantificar (datos perdidos, datos no identificados, no diligenciados o información perteneciente a entidades).
  """

  return text1, text2


def report_3(date_filter: list) -> Tuple[str,str]:

  q = f"""
              SELECT 
                a.sexo,
                COUNT(DISTINCT a.identificacion) AS cantidad
              FROM 
                AMISALUD_TM_MAESTRO_AFILIADOS a
                --JOIN Modulo_PQR_Sector_Salud b
                --ON CAST(a.identificacion AS varchar) = CAST(b.identificacion AS varchar)
              GROUP BY
                a.sexo
              ORDER BY
                cantidad DESC"""

  df = querier(q)
  date = datetime.strptime(date_filter[1], '%Y-%m-%d').date()
  year = date.strftime("%Y")
  month_name = (date.strftime("%B"))
  gender_dict = {'F':'femenino','M':'masculino'}

  # Creating plotly pie chart using the pre-processed data
  fig = px.pie(df, values='cantidad', names='sexo', hole=.3)
  fig.update_traces(textposition='inside')
  fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
  fig.update_layout(margin=dict(t=120, b=60, l=40, r=40),
                      plot_bgcolor='#fff',
                      uniformtext_minsize=8, uniformtext_mode='hide',
                      font={
                          'family': 'Rubik, sans-serif',
                          'color': '#515365'
                      },
                      title= f'Distribución de PQRS radicadas en secretaria de salud municipal de Ibague – Dirección de aseguramiento durante el {month_name} de {year}',
                      title_x=0.5,
                      title_font_family='Rubik, sans-serif',
                      title_font_size=15
                      )
  fig.write_image("assets/images/report_3.svg")

  # Text section
  text1 = f"""
  Se realiza la caracterización de la población que según la radicación de PQRS fueron radicadas durante el mes de {month_name.upper()} de {year}, identificando el género de mayor vulnerabilidad.
  """

  text2 = f"""
  Durante el mes de {month_name.upper()} de {year} se radicaron un total de {df['cantidad'].sum()} PQRS, se brindó más apoyo con un {round((df.loc[0,'cantidad'].values[0]/df['cantidad'].sum())*100,2)}% a las personas de género {gender_dict[df.loc[0,'cantidad'].values[0]]} ante la vulneración de sus derechos, en el caso del género {gender_dict[df.loc[1,'cantidad'].values[0]]} se brindo un apoyo del {round((df.loc[1,'cantidad'].values[0]/df['cantidad'].sum())*100,2)}%.
  """

  return text1, text2


def report_4(date_filter: list) -> Tuple[str,str]:

  try:
    q = f"""
        SELECT 
          CASE  
            WHEN glb_comunas_corregimientos.descripcion LIKE 'Corregimiento%' THEN 'Rural'
            ELSE glb_comunas_corregimientos.descripcion
          END as comuna, 
          COUNT(DISTINCT Modulo_PQR_Sector_Salud.id) as cantidad 
        FROM 
          Modulo_PQR_Sector_Salud 
          LEFT OUTER JOIN glb_barrios_veredas ON CAST(Modulo_PQR_Sector_Salud.glb_barrio_vereda_id AS varchar) = CAST(glb_barrios_veredas.id AS varchar) 
          LEFT OUTER JOIN glb_comunas_corregimientos ON CAST(glb_barrios_veredas.glb_comunas_corregimiento_id AS varchar) = CAST(glb_comunas_corregimientos.id AS varchar) 
          LEFT OUTER JOIN tipo_peticion ON CAST(Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_id AS varchar) = CAST(tipo_peticion.ID AS varchar)
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
    date = datetime.strptime(date_filter[1], '%Y-%m-%d').date()
    year = date.strftime("%Y")
    month_name = (date.strftime("%B"))
    df_comunas = df[df['comuna'].str.startswith('Comuna')].sort_values(by='cantidad', ascending=False).reset_index(drop=True)
    df_tail = df_comunas.tail(2).reset_index(drop=True)
    
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
                        title=f'Distribución de PQRS radicadas en la secretaria <br> de salud municipal de Ibagué - Dirección <br> de aseguramiento según comuna durante el mes de {month_name} de {year}',
                        title_x=0.5,
                        title_font_family='Rubik, sans-serif',
                        title_font_size=15
                        )
    fig.write_image("assets/images/report_4.svg")

    # Text section
    text1 = f"""
    Se realiza la caracterización de la población que según la radicación de PQRS del mes de {month_name.upper()} {year} se le han vulnerado sus derechos o sus requerimientos en salud, con esto podemos identificar qué comuna requiere apoyo.
    """

    text2 = f"""
    Durante el mes de {month_name.upper()} {year} se radicaron un total de {df['cantidad'].sum()} PQRS, de los cuales el {round((df_comunas.loc[0,'cantidad']/df['cantidad'].sum())*100,2)}% corresponde a la {df_comunas.loc[0,'comuna'].lower()}, {round((df_comunas.loc[1,'cantidad']/df['cantidad'].sum())*100,2)}% corresponde a la {df_comunas.loc[1,'comuna'].lower()}, {round((df_comunas.loc[2,'cantidad']/df['cantidad'].sum())*100,2)}% corresponden a la {df_comunas.loc[2,'comuna'].lower()} de Ibagué, donde los habitantes de estas comunas fueron los que más radicaron PQRS en busca del cumplimiento de sus derechos en salud.
    En este periodo de tiempo la {df_tail.loc[0,'comuna'].lower()} y la {df_tail.loc[1,'comuna'].lower()} de Ibagué presentaron el nivel más bajo de PQRS radicados en la Dirección de Aseguramiento de la Secretaria de Salud Municipal de Ibagué ya que no realizó la radicación de ninguna queja, reclamo o sugerencia.
    El {round((df.loc[df['comuna']=='Sin Informacion','cantidad'].values[0]/df['cantidad'].sum())*100,2)}% de PQRS radicados no cuentan con la información para ser tabulados, ya que no se encuentran identificados, diligenciados los datos o fueron radicados por entidades públicas o privadas las cuales no aplican en esta clasificación.
    """
  except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

  return text1, text2


def report_5(date_filter: list) -> Tuple[str,str]:

  q = f"""
        SELECT 
          CASE
            WHEN b.razon_social LIKE 'Sss Pijaos%' THEN 'Pijao Salud EPS'
            WHEN b.razon_social LIKE 'Eps Pijao Salud%' THEN 'Pijao Salud EPS'
            WHEN b.razon_social LIKE 'SSS salud total%' THEN 'Salud Total EPS'
            WHEN b.razon_social LIKE 'Salud Total%' THEN 'Salud Total EPS'
            WHEN b.razon_social LIKE 'SSS E.P.S. sanitas%' THEN 'Sanitas EPS'
            WHEN b.razon_social LIKE 'Salud Sanitas%' THEN 'Sanitas EPS'
            WHEN b.razon_social LIKE 'SSS Coomeva EPS%' THEN 'Coomeva EPS'
            WHEN b.razon_social LIKE 'Coomeva Eps%' THEN 'Coomeva EPS'
            WHEN b.razon_social LIKE 'Eps Famisanar%' THEN 'Famisanar EPS'
            WHEN b.razon_social LIKE 'Medimas EPS%' THEN 'Medimas EPS'
            WHEN b.razon_social LIKE 'Nueva EPS%' THEN 'Nueva EPS'
            WHEN b.razon_social LIKE 'Nueva Eps%' THEN 'Nueva EPS'
            ELSE 'Sin Informacion'
          END AS entidad,
          COUNT(DISTINCT a.id) AS cantidad
        FROM 
          Modulo_PQR_Sector_Salud a
          LEFT OUTER JOIN glb_entidads b ON CAST(a.glb_entidad_id AS varchar) = CAST(b.id AS varchar)
        WHERE 
          to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'
        GROUP BY 
          entidad
        ORDER BY
          cantidad DESC"""

  df = querier(q)
  date = datetime.strptime(date_filter[1], '%Y-%m-%d').date()
  year = date.strftime("%Y")
  month_name = (date.strftime("%B"))

  # Creating plotly pie chart
  fig = px.pie(df, values='cantidad', names='entidad')
  fig.update_traces(textposition='outside')
  fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
  fig.update_layout(margin=dict(t=120, b=60, l=40, r=40),
                      plot_bgcolor='#fff',
                      uniformtext_minsize=8, uniformtext_mode='hide',
                      font={
                          'family': 'Rubik, sans-serif',
                          'color': '#515365'
                      },
                      title= f'PQRS radicadas en relación a la EPS recibidas en <br> secretaria de salud municipal de Ibagué - Dirección de <br> aseguramiento durante el mes de {month_name} de {year}',
                      title_x=0.5,
                      title_font_family='Rubik, sans-serif',
                      title_font_size=15
                      )
  fig.write_image("assets/images/report_5.svg")

  # Text section
  text1 = f"""
  El total de PQRS radicados durante el mes de {month_name.upper()} {year}, en relación con la EAPB implícita en el proceso de gestión, así se realizará la evaluación por entidad identificando cuál de estas requiere mayor vigilancia y control.
  """

  text2 = f"""
  Durante el mes de {month_name.upper()} de {year} se radicaron un total de {df['cantidad'].sum()} PQRS, la EAPB en la que los usuarios en salud requirieron más apoyo para el cumplimiento de sus derechos fue {df.loc[0,'entidad'].upper()} con un {round((df.loc[0,'cantidad']/df['cantidad'].sum())*100,2)}%, seguido de {df.loc[1,'entidad'].upper()} con un {round((df.loc[1,'cantidad']/df['cantidad'].sum())*100,2)}%.

  El {round((df.loc[df['entidad']=='Sin Informacion','cantidad'].values[0]/df['cantidad'].sum())*100,2)}% de PQRS radicados no cuentan con la información para ser tabulados, ya que no se encuentran identificados o diligenciados los datos.
  """

  return text1, text2


def report_6(date_filter: list) -> Tuple[str,str]:

  q = f"""
          SELECT 
            CASE
              WHEN b.TIPO_PETICION IN ('Queja','Denuncia') THEN 'Queja'
              WHEN b.TIPO_PETICION IS NOT NULL THEN b.TIPO_PETICION
              ELSE 'Sin Informacion'
            END AS tipo,
            COUNT(DISTINCT a.id) as cantidad
          FROM 
            Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
          WHERE 
            to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'
          GROUP BY
            tipo
          ORDER BY
            cantidad DESC"""

  df = querier(q)
  df_chart = df[df['tipo'] != 'Sin Informacion']
  date = datetime.strptime(date_filter[1], '%Y-%m-%d').date()
  year = date.strftime("%Y")
  month_name = (date.strftime("%B"))

  # Creating plotly pie chart using the pre-processed data
  fig = px.pie(df_chart, values='cantidad', names='tipo', hole=.3)
  fig.update_traces(textposition='inside')
  fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
  fig.update_layout(margin=dict(t=120, b=60, l=40, r=40),
                      plot_bgcolor='#fff',
                      uniformtext_minsize=8, uniformtext_mode='hide',
                      font={
                          'family': 'Rubik, sans-serif',
                          'color': '#515365'
                      },
                      title= f'PQRS radicadas en relación al tipo recibidas en la <br> secretaria de salud municipal de ibague - dirección  <br> de aseguramiento durante el mes de {month_name} de {year}',
                      title_x=0.5,
                      title_font_family='Rubik, sans-serif',
                      title_font_size=15
                      )
  fig.write_image("assets/images/report_6.svg")

  # Text section
  text1 = f"""
  El total de PQRS radicados en relación con su tipo, radicados durante el mes de {month_name.upper()} de {year}.
  """

  text2 = f"""
  Durante el mes de {month_name.upper()} de {year} se radicaron un total de {df['cantidad'].sum()} PQRS, el tipo de PQRS que más se radicó fue la de {df.loc[0,'tipo']} en un {round((df.loc[0,'cantidad']/df['cantidad'].sum())*100,2)}%; seguido de {df.loc[1,'tipo']} con un {round((df.loc[1,'cantidad']/df['cantidad'].sum())*100,2)}%.
  """

  return text1, text2


def report_8(date_filter: list) -> Tuple[str,str]:

  q = f"""
            SELECT 
              CASE b.descripcion 
                WHEN 'Radicado' THEN 'En Tramite'
                WHEN 'Digitalizado' THEN 'En Tramite'
                WHEN 'En Tramite' THEN 'En Tramite'
                WHEN 'Proceso cerrado' THEN 'Resuelto'
                WHEN 'Resuelto' THEN 'Resuelto'
                WHEN 'Documentos sin respuesta' THEN 'Resuelto' 
              END as estado, 
              COUNT(DISTINCT a.id) as cantidad
            FROM 
              Modulo_PQR_Sector_Salud a
              LEFT OUTER JOIN glb_estados b ON CAST(a.glb_estado_id AS varchar) = CAST(b.id AS varchar)
            WHERE 
            to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'
            GROUP BY
              estado"""

  df = querier(q)
  date = datetime.strptime(date_filter[1], '%Y-%m-%d').date()
  year = date.strftime("%Y")
  month_name = (date.strftime("%B"))

  # Creating plotly bar chart using the pre-processed data
  fig = px.bar(df, x="estado", y="cantidad", orientation='v',
      labels={"estado": "Estado",
              "cantidad": "Cantidad"}
  )
  fig.update_traces(texttemplate='%{y}', textposition='inside')
  fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
  fig.update_layout(
                      plot_bgcolor='#fff',
                      uniformtext_minsize=8, uniformtext_mode='hide',
                      font={
                          'family': 'Rubik, sans-serif',
                          'color': '#515365'
                      },
                      title=f'PQRS radicadas en relación a estado de respuesta recibidas <br> en secretaria de salud municipal de ibague - dirección  <br> de aseguramiento durante el mes de {month_name} de {year}',
                      title_x=0.5,
                      title_font_family='Rubik, sans-serif',
                      title_font_size=15
                      )
  fig.write_image("assets/images/report_8.svg")

  # Text section
  text1 = f"""
  Analizar la cantidad de PQRS que a la fecha se encuentran resueltos radicados durante el mes de {month_name.upper()} de {year}, y que nos permita así analizar la oportunidad de gestión.
  """

  text2 = f"""
  Durante el mes de {month_name.upper()} de {year} se radicaron un total de {df['cantidad'].sum()} PQRS, a la fecha se encuentran resueltos en el {round((df.loc[df['estado']=='Resuelto','cantidad'].values[0]/df['cantidad'].sum())*100,2)}% de los casos y se encuentran en trámite en un {round((df.loc[df['estado']=='En Tramite','cantidad'].values[0]/df['cantidad'].sum())*100,2)}%.
  """

  return text1, text2