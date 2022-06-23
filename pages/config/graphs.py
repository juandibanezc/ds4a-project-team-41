from dash import html, dcc, Input, Output, State, ALL, MATCH
import dash_mantine_components as dmc
from dash import html, dcc
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from pages.config import model
import calendar
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import nltk
from wordcloud import WordCloud
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.corpus import stopwords
#nltk.download('punkt')
import json
#import controller
def dateFilter(id):
  output = [
              html.Div(children=[
                  dmc.DateRangePicker(
                              id={'type':"date-range-picker","index":id},
                              value=[(date.today().replace(month=1).replace(day=1)).strftime('%Y-%m-%d'),(date.today().replace(month=12).replace(day=calendar.monthrange(date.today().year, 12)[1])).strftime('%Y-%m-%d')],
                              amountOfMonths=2,
                              dropdownType="modal",
                              zIndex=1000,
                              shadow='sm',
                              modalZIndex=1000,
                              allowSingleDateInRange = True,
                              class_name=""

                  )
              ])
    ]

  return output

def graph_seguimiento_pqrs(df):
    """
    toma como argumento una ruta a base de datos pqr, y devuelve un elemento figura con la grafica de seguimiento de pqrs
    """
    
    df['fecha_radicacion'] = pd.to_datetime(df['fecha_radicacion'])
    df["mes"] = df['fecha_radicacion'].dt.month_name()

    df_g = df.groupby(['mes','estado']).agg(pqr_count=('fecha_radicacion', 'count'))
    df_g = df_g.sort_values(by='mes').reset_index(drop=False)
    fig = px.line(df_g, x="mes", y="pqr_count", color='estado',
        labels={"mes": "Mes",
                "pqr_count": "Cantidad de PQRs",
                "estado": "Estado de la PQR"}
    )
    fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
    fig.update_layout(
                       plot_bgcolor='#fff',
                       font={
                           'family': 'Rubik, sans-serif',
                           'color': '#515365'
                       },
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig

def graph_distribucion_eps(df):

    df_g = df.groupby(['EPS']).agg(pqr_count=('id', 'count'))
    df_g = df_g.sort_values(by='pqr_count').reset_index(drop=False)
    fig = px.bar(df_g, x="pqr_count", y="EPS", orientation='h',
        labels={"EPS": "EPS",
                "pqr_count": "Cantidad de PQRs"}
    )
    fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
    fig.update_layout(
                       plot_bgcolor='#fff',
                       font={
                           'family': 'Rubik, sans-serif',
                           'color': '#515365'
                       },
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig


def graph_distribucion_sisben(df):

    df['sisben'] = df['sisben'].str[0]
    df_g = df.groupby(['sisben']).agg(pqr_count=('ID', 'count'))
    df_g = df_g.sort_values(by='pqr_count').reset_index(drop=False)
    fig = px.pie(df_g, values='pqr_count', names='sisben')
    fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
    fig.update_layout(
                       plot_bgcolor='#fff',
                       font={
                           'family': 'Rubik, sans-serif',
                           'color': '#515365'
                       },
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig


def graph_distribucion_sexo(df):

    df_g = df.groupby(['SEXO']).agg(pqr_count=('ID', 'count'))
    df_g = df_g.sort_values(by='pqr_count').reset_index(drop=False)
    fig = px.pie(df_g, values='pqr_count', names='SEXO')
    fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
    fig.update_layout(
                       plot_bgcolor='#fff',
                       font={
                           'family': 'Rubik, sans-serif',
                           'color': '#515365'
                       },
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig


def graph_distribucion_edad(df):

    df.FECHA_NACIMIENTO=pd.to_datetime(df.FECHA_NACIMIENTO)
    df['edad']=(datetime.now()-df.FECHA_NACIMIENTO).dt.days/365.25
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
      

    df_g = df.groupby(['edad_str']).agg(pqr_count=('ID', 'count'))
    df_g = df_g.sort_values(by='pqr_count',ascending=False).reset_index(drop=False)
    fig = px.funnel(df_g, x='pqr_count', y='edad_str', labels={'edad_str':'Edad'})
    fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
    fig.update_layout(
                       plot_bgcolor='#fff',
                       font={
                           'family': 'Rubik, sans-serif',
                           'color': '#515365'
                       },
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig

# def tipo_pqr_vs_eps(ruta):
#     transaccion="""SELECT tipo_peticion.TIPO_PETICION, glb_entidads.razon_social 
#     FROM Modulo_PQR_Sector_Salud JOIN glb_entidads 
#     ON Modulo_PQR_Sector_Salud.glb_entidad_id=glb_entidads.id JOIN tipo_peticion ON 
#     Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_id=tipo_peticion.ID
#     """
#     a=controller.query(ruta,transaccion)
#     df=pd.crosstab(a["razon_social"],a["TIPO_PETICION"])
#     fig=px.imshow(df,aspect="auto",labels=dict(x="Tipo de peticion", y="Entidad prestadora de salud", color="Numero de peticiones"))
#     return fig    

# def distribucion_pqrs_comunas(ruta):
#     transaccion="""SELECT tipo_peticion.TIPO_PETICION, glb_comunas_corregimientos.descripcion 
#     FROM Modulo_PQR_Sector_Salud JOIN glb_barrios_veredas 
#     ON Modulo_PQR_Sector_Salud.glb_barrio_vereda_id= glb_barrios_veredas.id JOIN glb_comunas_corregimientos ON 
#     glb_barrios_veredas.glb_comunas_corregimiento_id=glb_comunas_corregimientos.id JOIN tipo_peticion ON 
#     Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_id=tipo_peticion.ID
#     """
#     a=controller.query(ruta,transaccion)
#     df=pd.crosstab(a["descripcion"],a["TIPO_PETICION"])
#     df=df.reset_index()
#     df=df[df["descripcion"].isin(['Comuna 1',"Comuna 2","Comuna 3","Comuna 4","Comuna 5","Comuna 6","Comuna 7","Comuna 8","Comuna 9","Comuna 10","Comuna 11"])]
#     df=df.set_index("descripcion")
#     #df=df.drop(columns=["TIPO_PETICION"])
#     df=df.sort_index(axis=0,ascending=True)
#     fig=px.imshow(df,aspect="auto",labels=dict(x="Tipo de peticion", y="Entidad prestadora de salud", color="Numero de peticiones"))

#     return fig
    
# def graph_heatmap_estado_dependence(ruta):
#      """
#      Toma como argumento la ruta de la bse de datos de pqr, y devuelve un elemento plotly fig con el heatmap 
#      entre estado y dependencia
#      """
#      b=controller.query(ruta,"""SELECT glb_dependencia_id, CASE
#          glb_estado_id
#                              WHEN 1 THEN "Radicado"
#                              WHEN 2 THEN "Digitalizado"
#                              WHEN 3 THEN "En tramite"
#                              WHEN 4 THEN "Proceso cerrado"
#                              WHEN 5 THEN "Resuelto"
#                              WHEN 6 THEN "Documento sin resp"
#          END AS estado FROM Modulo_PQR_Sector_Salud""")
#      b.glb_dependencia_id=b.glb_dependencia_id.astype("string")
#      estado_vs_dependencia = pd.crosstab(b["estado"], b["glb_dependencia_id"], normalize = 'columns')
#      fig=px.imshow(estado_vs_dependencia, title="PQR processing stage (normalized for each dependence)",aspect="auto",labels=dict(x="glb_dependencia_id", y="Estado", color="processing stage"))
#      return fig

    
# def clean_word_cloud(ruta): 
    
#      c=controller.query(ruta,"""SELECT asunto FROM Modulo_PQR_Sector_Salud""")
#      ### Getting a single string
#      esp_stopwords = stopwords.words("spanish")
#      nombre_text = ' '.join(c["asunto"].dropna())
#      ## Splitting them into tokens
#      word_tokens = nltk.word_tokenize(nombre_text)
#      ## Removing the stopwords
#      nombre_word_tokens_clean = [each for each in word_tokens if each.lower() not in esp_stopwords and len(each.lower()) > 2]

#      word_cloud_text = ' '.join(nombre_word_tokens_clean)
#      wordcloud = WordCloud(max_font_size=100, max_words=40, background_color="white",\
#                                scale = 10,width=800, height=400).generate(word_cloud_text)

#      fig=px.imshow(wordcloud,aspect="auto")
#      fig.update_xaxes(visible=False)
#      fig.update_yaxes(visible=False)
#      return fig

    
# def graf_tipo_solicitud(ruta):
#     """
#     Esta funcion recibe como argumento la ruta de la db, y devuelve 4 graficas, segun el tipo de solicitud, por mes
#     en el siguiente orden:
#     "Denuncias","Solicitudes","Quejas","Reclamos"
    
    
#     """
#     transaccion="""SELECT Modulo_PQR_Sector_Salud.asunto, Modulo_PQR_Sector_Salud.fecha_radicacion, tipo_peticion.TIPO_PETICION 
#     FROM Modulo_PQR_Sector_Salud JOIN tipo_peticion 
#     ON Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_especifica_id=tipo_peticion.id"""
#     a=query(ruta,transaccion)
#     a.fecha_radicacion=pd.to_datetime(a.fecha_radicacion).dt.month_name()
#     solicitudes=['Denuncia', 'Solicitud', 'Queja', 'Reclamo']
#     titles=["Denuncias","Solicitudes","Quejas","Reclamos"]
#     i=0
#     figuras=[]
#     for solicitud in solicitudes:
#         df_temp=a[a.TIPO_PETICION==solicitud]
#         df_temp=df_temp.groupby("fecha_radicacion").agg({"TIPO_PETICION":len})
#         df_temp=df_temp.reset_index()
#         df_temp=df_temp.rename(columns={"TIPO_PETICION":"Cuenta"})
#         fig=px.bar(df_temp, x='fecha_radicacion', y='Cuenta',title=titles[i])
#         fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
#         figuras.append(fig)
#         i=i+1
#     return figuras
# def distribucion_por_sisben(ruta):
#     transaccion="""SELECT ID, PUNTAJE FROM AMISALUD_TM_SISBEN_MENSUAL"""
#     a=query(r"C:\Users\pablo\Desktop\BASE DATOS IBAGUE\BDIBAGUE.db",transaccion)
#     a=a.groupby("PUNTAJE").agg({"ID":len})
#     a=a.reset_index()
#     a=a.sort_values(by='PUNTAJE',ascending=True)
#     fig = px.pie(a, values='ID', names='PUNTAJE', title='Distribucion por SISBEN',width=800, height=800)
#     return fig
# def graf_tipo_solicitud(ruta):
#     """
#      Esta funcion recibe como argumento la ruta de la db, y devuelve 4 graficas, segun el tipo de solicitud, por mes
#      en el siguiente orden:
#      "Denuncias","Solicitudes","Quejas","Reclamos"
#     """
#     transaccion="""SELECT Modulo_PQR_Sector_Salud.asunto, Modulo_PQR_Sector_Salud.fecha_radicacion, tipo_peticion.TIPO_PETICION 
#     FROM Modulo_PQR_Sector_Salud JOIN tipo_peticion 
#     ON Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_especifica_id=tipo_peticion.id"""
#     a=controller.query(ruta,transaccion)
#     a.fecha_radicacion=pd.to_datetime(a.fecha_radicacion).dt.month_name()
#     solicitudes=['Denuncia', 'Solicitud', 'Queja', 'Reclamo']
#     titles=["Denuncias","Solicitudes","Quejas","Reclamos"]
#     i=0
#     figuras=[]
#     for solicitud in solicitudes:
#         df_temp=a[a.TIPO_PETICION==solicitud]
#         df_temp=df_temp.groupby("fecha_radicacion").agg({"TIPO_PETICION":len})
#         df_temp=df_temp.reset_index()
#         df_temp=df_temp.rename(columns={"TIPO_PETICION":"Cuenta"})
#         fig=px.bar(df_temp, x='fecha_radicacion', y='Cuenta',title=titles[i])
#         fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
#         figuras.append(fig)
#         i=i+1
#     return figuras
# def distribucion_por_sisben(ruta):
#     transaccion="""SELECT ID, PUNTAJE FROM AMISALUD_TM_SISBEN_MENSUAL"""
#     a=controller.query(r"C:\Users\pablo\Desktop\BASE DATOS IBAGUE\BDIBAGUE.db",transaccion)
#     a=a.groupby("PUNTAJE").agg({"ID":len})
#     a=a.reset_index()
#     a=a.sort_values(by='PUNTAJE',ascending=True)
#     fig = px.pie(a, values='ID', names='PUNTAJE', title='Distribucion por SISBEN',width=800, height=800)
#     return fig



    
