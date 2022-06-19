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
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.corpus import stopwords
nltk.download('punkt')
import json

def dateFilter(id):
  output = [
              html.Div(className="col-8 p-0",children=[
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

def graph_seguimiento_pqrs(query, ruta_db):
    """
    toma como argumento una ruta a base de datos pqr, y devuelve un elemento figura con la grafica de seguimiento de pqrs
    """
    
    df = model.querier(ruta_db, query)
    df['fecha_radicacion'] = pd.to_datetime(df['fecha_radicacion'])
    df["mes"] = df['fecha_radicacion'].dt.month_name()

    df_g = df.groupby(['mes','estado']).agg(pqr_count=('fecha_radicacion', 'count'))
    df_g = df_g.reset_index(drop=False)
    fig = px.line(df_g, x="mes", y="pqr_count", color='estado',
        labels={"mes": "Mes",
                "pqr_count": "Cantidad de PQRs",
                "estado": "Estado de la PQR"}
    )
    return fig

    
# def graph_heatmap_estado_dependence(ruta):
#     """
#     Toma como argumento la ruta de la bse de datos de pqr, y devuelve un elemento plotly fig con el heatmap 
#     entre estado y dependencia
#     """
#     b=query(ruta,"""SELECT glb_dependencia_id, CASE
#         glb_estado_id
#                             WHEN 1 THEN "Radicado"
#                             WHEN 2 THEN "Digitalizado"
#                             WHEN 3 THEN "En tramite"
#                             WHEN 4 THEN "Proceso cerrado"
#                             WHEN 5 THEN "Resuelto"
#                             WHEN 6 THEN "Documento sin resp"
#         END AS estado FROM Modulo_PQR_Sector_Salud""")
#     b.glb_dependencia_id=b.glb_dependencia_id.astype("string")
#     estado_vs_dependencia = pd.crosstab(b["estado"], b["glb_dependencia_id"], normalize = 'columns')
#     fig=px.imshow(estado_vs_dependencia, title="PQR processing stage (normalized for each dependence)",aspect="auto",labels=dict(x="glb_dependencia_id", y="Estado", color="processing stage"))
#     return fig

    
# def clean_word_cloud(ruta): 
#     c=query(ruta,"""SELECT asunto FROM Modulo_PQR_Sector_Salud""")
#     ### Getting a single string
#     esp_stopwords = stopwords.words("spanish")
#     nombre_text = ' '.join(c["asunto"].dropna())
#     ## Splitting them into tokens
#     word_tokens = nltk.word_tokenize(nombre_text)
#     ## Removing the stopwords
#     nombre_word_tokens_clean = [each for each in word_tokens if each.lower() not in esp_stopwords and len(each.lower()) > 2]

#     word_cloud_text = ' '.join(nombre_word_tokens_clean)
#     wordcloud = WordCloud(max_font_size=100, max_words=40, background_color="white",\
#                               scale = 10,width=800, height=400).generate(word_cloud_text)

#     fig=px.imshow(wordcloud,aspect="auto")
#     fig.update_xaxes(visible=False)
#     fig.update_yaxes(visible=False)
#     return fig

    
# def graf_tipo_solicitud(ruta):
#     """
#     Esta funcion recibe como argumento la ruta de la db, y devuelve 4 graficas, segun el tipo de solicitud, por mes
#     en el siguiente orden:
#     "Denuncias","Solicitudes","Quejas","Reclamos"
    
    
    """
    transaccion="""SELECT Modulo_PQR_Sector_Salud.asunto, Modulo_PQR_Sector_Salud.fecha_radicacion, tipo_peticion.TIPO_PETICION 
    FROM Modulo_PQR_Sector_Salud JOIN tipo_peticion 
    ON Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_especifica_id=tipo_peticion.id"""
    a=query(ruta,transaccion)
    a.fecha_radicacion=pd.to_datetime(a.fecha_radicacion).dt.month_name()
    solicitudes=['Denuncia', 'Solicitud', 'Queja', 'Reclamo']
    titles=["Denuncias","Solicitudes","Quejas","Reclamos"]
    i=0
    figuras=[]
    for solicitud in solicitudes:
        df_temp=a[a.TIPO_PETICION==solicitud]
        df_temp=df_temp.groupby("fecha_radicacion").agg({"TIPO_PETICION":len})
        df_temp=df_temp.reset_index()
        df_temp=df_temp.rename(columns={"TIPO_PETICION":"Cuenta"})
        fig=px.bar(df_temp, x='fecha_radicacion', y='Cuenta',title=titles[i])
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        figuras.append(fig)
        i=i+1
    return figuras
def distribucion_por_sisben(ruta):
    transaccion="""SELECT ID, PUNTAJE FROM AMISALUD_TM_SISBEN_MENSUAL"""
    a=query(r"C:\Users\pablo\Desktop\BASE DATOS IBAGUE\BDIBAGUE.db",transaccion)
    a=a.groupby("PUNTAJE").agg({"ID":len})
    a=a.reset_index()
    a=a.sort_values(by='PUNTAJE',ascending=True)
    fig = px.pie(a, values='ID', names='PUNTAJE', title='Distribucion por SISBEN',width=800, height=800)
    return fig
    
