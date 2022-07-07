from plotly.graph_objs._figure import Figure
import plotly.express as px
from pages.config.model import split_index
from datetime import datetime
import geopandas as gpd
import pandas as pd


def graph_seguimiento_pqrs(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a line chart that tracks the state of the PQRS through time.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure line chart.
    """
    
    # Getting month component of each date and grouping the data by month
    df['fecha_radicacion'] = pd.to_datetime(df['fecha_radicacion'])
    df["mes"] = df['fecha_radicacion'].dt.to_period('M')
    df["mes"] = df["mes"].astype('string')
    df_g = df.groupby(['mes','estado'], as_index=False).agg(pqr_count=('fecha_radicacion', 'count'))
    df_g = df_g.sort_values(by='mes', ascending=True).reset_index(drop=False)

    # Creating plotly line chart using the pre-processed data
    fig = px.line(df_g, x="mes", y="pqr_count", color='estado',
                      labels={"mes": "Mes",
                              "pqr_count": "Cantidad de PQRS",
                              "estado": "Estado de la PQR"}
                  )
    fig.update_traces(mode='markers+lines')
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


def graph_mapa_comunas(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a choropleth map chart that shows the amount of PQRS per comuna.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure choropleth map chart.
    """

    # Setting id of each comuna in the dataframe equals to their id in the geojson file
    df['id'] = df['id'].str.replace(" ","").str.lower()
    comunas = gpd.read_file('assets/json/comunas_ibague.geojson')

    # Merging the amount of PQRS in the dataframe into the geojson file
    comunas = comunas.merge(df, how='left', on='id')
    comunas = comunas.set_index('id')

    # Creating plotly choropleth map chart using the pre-processed data
    fig = px.choropleth(comunas, 
                        geojson=comunas.geometry, 
                        locations=comunas.index, 
                        color="cantidad", 
                        projection="mercator", 
                        color_continuous_scale="Viridis")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


def graph_distribucion_entidad(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a bar chart that shows the amount of PQRS per health entity.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure bar chart.
    """

    # Grouping the data by health entity
    df_g = df.groupby(['entidad'], as_index=False).agg(pqr_count=('id', 'count'))
    df_g = df_g.sort_values(by='pqr_count').reset_index(drop=False)
    df_g['entidad'] = df_g['entidad'].str.split(' ').apply(lambda x: ' '.join(x[:2])) #TODO: change this for the data cleaning from Pablo

    # Creating plotly bar chart using the pre-processed data
    fig = px.bar(df_g, x="entidad", y="pqr_count", orientation='v',
        labels={"entidad": "Entidad",
                "pqr_count": "Cantidad de PQRS"}
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


def graph_distribucion_sisben(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a pie chart that shows the amount of PQRS per Sisben group.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure pie chart.
    """

    # Getting the group out of Sisben score and grouping the data by Sisben group
    df['grupo'] = df['grupo'].str[0]
    df_g = df.groupby(['grupo']).agg(pqr_count=('identificacion', 'count'))
    df_g = df_g.sort_values(by='pqr_count').reset_index(drop=False)

    # Creating plotly pie chart using the pre-processed data
    fig = px.pie(df_g, values='pqr_count', names='grupo')
    fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
    fig.update_layout(margin=dict(t=60, b=60, l=60, r=60),
                       plot_bgcolor='#fff',
                       font={
                           'family': 'Rubik, sans-serif',
                           'color': '#515365'
                       },
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig


def graph_distribucion_sexo(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a pie chart that shows the amount of PQRS per sex.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure pie chart.
    """

    # Grouping the data by sex
    df_g = df.groupby(['sexo']).agg(cantidad=('identificacion', 'count'))
    df_g = df_g.sort_values(by='cantidad').reset_index(drop=False)

    # Creating plotly pie chart using the pre-processed data
    fig = px.pie(df_g, values='cantidad', names='sexo')
    fig.update_layout(legend=dict(traceorder='reversed', font_size=9))
    fig.update_layout(margin=dict(t=60, b=60, l=60, r=60),
                       plot_bgcolor='#fff',
                       font={
                           'family': 'Rubik, sans-serif',
                           'color': '#515365'
                       },
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig


def graph_distribucion_edad(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a funnel chart that shows the amount of PQRS per age range.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure funnel chart.
    """

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
                       title_font_family='Rubik, sans-serif',
                       title_font_size=15
                       )

    return fig


def graph_distribucion_tipo_peticion_comuna(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a heatmap chart that shows the amount of PQRS per petition type and comuna.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure heatmap chart.
    """

    # Creating cross table and filtering data of interest
    df=pd.crosstab(df["descripcion"],df["tipo_peticion"])
    df=df.reset_index()
    df=df[df["descripcion"].isin(['Comuna 1',"Comuna 2","Comuna 3","Comuna 4","Comuna 5","Comuna 6","Comuna 7","Comuna 8","Comuna 9","Comuna 10","Comuna 11","Comuna 12","Comuna 13"])]

    # Cleaning values and sorting them
    df['descripcion'] = df['descripcion'].str.replace("Comuna ","C")
    df['order'] = df['descripcion'].map(split_index)
    df.sort_values('order', inplace=True)
    df.drop('order', axis=1, inplace=True)
    df.set_index('descripcion', inplace=True)

    # Creating plotly image data of the crosstable using the pre-processed data
    fig=px.imshow(df,aspect="auto",labels=dict(x="Tipo de peticion", y="Comuna", color="Cantidad"))
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


def graph_distribucion_tipo_peticion_entidad(df: pd.DataFrame) -> Figure:
    """
    Preprocess the data and creates a heatmap chart that shows the amount of PQRS per petition type and health entity.
    
    Args:
        df: Data to be pre-processed and used as input for the chart.
    Returns:
        fig: Plotly Figure heatmap chart.
    """

    # Creating cross table
    df['entidad'] = df['entidad'].str.split(' ').apply(lambda x: ' '.join(x[:2])) #TODO: change this for the data cleaning from Pablo
    df=pd.crosstab(df["entidad"],df["tipo_peticion"])
    
    # Creating plotly image data of the crosstable using the pre-processed data
    fig=px.imshow(df,aspect="auto",labels=dict(x="Tipo de peticion", y="Entidad prestadora de salud", color="Cantidad"))
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