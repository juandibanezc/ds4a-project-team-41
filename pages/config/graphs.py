import pandas as pd
import plotly.express as px
import nltk
from wordcloud import WordCloud
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.corpus import stopwords
nltk.download('punkt')
import json

def graph_seguimiento_pqrs(ruta_db):
    """
    toma como argumento una ruta a base de datos pqr, y devuelve un elemento figura con la grafica de seguimiento de pqrs
    """
    transaccion="""SELECT CASE glb_estado_id
                            WHEN 1 THEN "Radicado"
                            WHEN 2 THEN "Digitalizado"
                            WHEN 3 THEN "En tramite"
                            WHEN 4 THEN "Proceso cerrado"
                            WHEN 5 THEN "Resuelto"
                            WHEN 6 THEN "Documento sin resp"
                        END AS estado, updated_at FROM Modulo_PQR_Sector_Salud"""
    a=query(ruta_db,transaccion)
    a.updated_at=pd.to_datetime(a.updated_at)
    a["mes"]=a.updated_at.dt.month_name()
    a=a.groupby(['mes','estado']).agg({"updated_at":len})
    a=a.reset_index()
    a=a.sort_values(by=["updated_at"],ascending=False)
    a=a.rename(columns={"updated_at":"Cuenta"})
    fig = px.bar(a, x='mes', y='Cuenta',color="estado")
    return fig
def graph_heatmap_estado_dependence(ruta):
    """
    Toma como argumento la ruta de la bse de datos de pqr, y devuelve un elemento plotly fig con el heatmap 
    entre estado y dependencia
    """
    b=query(ruta,"""SELECT glb_dependencia_id, CASE
        glb_estado_id
                            WHEN 1 THEN "Radicado"
                            WHEN 2 THEN "Digitalizado"
                            WHEN 3 THEN "En tramite"
                            WHEN 4 THEN "Proceso cerrado"
                            WHEN 5 THEN "Resuelto"
                            WHEN 6 THEN "Documento sin resp"
        END AS estado FROM Modulo_PQR_Sector_Salud""")
    b.glb_dependencia_id=b.glb_dependencia_id.astype("string")
    estado_vs_dependencia = pd.crosstab(b["estado"], b["glb_dependencia_id"], normalize = 'columns')
    fig=px.imshow(estado_vs_dependencia, title="PQR processing stage (normalized for each dependence)",aspect="auto",labels=dict(x="glb_dependencia_id", y="Estado", color="processing stage"))
    return fig
def clean_word_cloud(ruta): 
    c=query(ruta,"""SELECT asunto FROM Modulo_PQR_Sector_Salud""")
    ### Getting a single string
    esp_stopwords = stopwords.words("spanish")
    nombre_text = ' '.join(c["asunto"].dropna())
    ## Splitting them into tokens
    word_tokens = nltk.word_tokenize(nombre_text)
    ## Removing the stopwords
    nombre_word_tokens_clean = [each for each in word_tokens if each.lower() not in esp_stopwords and len(each.lower()) > 2]

    word_cloud_text = ' '.join(nombre_word_tokens_clean)
    wordcloud = WordCloud(max_font_size=100, max_words=40, background_color="white",\
                              scale = 10,width=800, height=400).generate(word_cloud_text)

    fig=px.imshow(wordcloud,aspect="auto")
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig