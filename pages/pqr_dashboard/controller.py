import pandas as pd
import dash
from dash import html, dcc, Input, Output, State, ALL, MATCH
import time
import numpy as np
from app import app
from datetime import datetime
from pages.config import model, graphs


# **** KPI 1 ****
@app.callback([Output('peticiones_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_1(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT COUNT(DISTINCT a.id) as peticiones 
            FROM Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE b.TIPO_PETICION IN ('Peticion')"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r,query=q)
            kpi_output = df.loc[0,'peticiones']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** KPI 2 ****
@app.callback([Output('sugerencias_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_2(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT COUNT(DISTINCT a.id) as sugerencias 
            FROM Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE b.TIPO_PETICION IN ('Solicitud')"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r,query=q)
            kpi_output = df.loc[0,'sugerencias']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** KPI 3 ****
@app.callback([Output('reclamos_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_3(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT COUNT(DISTINCT a.id) as reclamos 
            FROM Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE b.TIPO_PETICION IN ('Reclamo')"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r,query=q)
            kpi_output = df.loc[0,'reclamos']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** KPI 4 ****
@app.callback([Output('quejas_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_4(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT COUNT(DISTINCT a.id) as quejas 
            FROM Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE b.TIPO_PETICION IN ('Queja','Denuncia')"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r,query=q)
            kpi_output = df.loc[0,'quejas']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** Graph 1 ****
@app.callback([Output('seguimientoPQR_graph','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_seguimiento_pqrs(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT 
            CASE b.descripcion 
            WHEN 'Radicado' THEN 'En Tramite'
            WHEN 'Digitalizado' THEN 'En Tramite'
            WHEN 'En Tramite' THEN 'En Tramite'
            WHEN 'Proceso cerrado' THEN 'Resuelto'
            WHEN 'Resuelto' THEN 'Resuelto'
            WHEN 'Documentos sin respuesta' THEN 'Resuelto' END as estado, 
            fecha_radicacion 
            FROM Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN glb_estados b ON a.glb_estado_id = b.id"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r, query=q)

            fig = graphs.graph_seguimiento_pqrs(df)
            graph_output = [dcc.Graph(id='seguimientoPQR_graph',
                                      figure=fig,
                                      config={'displaylogo': False})]

        else:
            graph_output= ['An error ocurred, please try again']

        return [graph_output]


# # **** Graph 2 ****
# @app.callback([Output('distribucionPQRCOMUNA_graph','children')],
#               [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
#                Input('url', 'pathname')])
# def graph_distribucion_comunas(date_filter,url):

#         if url == '/pqr_dashboard':

#             q = """
#             SELECT 
#             fecha_radicacion 
#             FROM Modulo_PQR_Sector_Salud a
#             LEFT OUTER JOIN glb_estados b ON a.glb_estado_id = b.id"""
#             r = "./BDIBAGUE.db"
#             df = model.querier(ruta_db=r, query=q)

#             fig = graphs.graph_seguimiento_pqrs(df)
#             graph_output = [dcc.Graph(id='seguimientoPQR_graph',
#                                       figure=fig,
#                                       config={'displaylogo': False})]

#         else:
#             graph_output= ['An error ocurred, please try again']

#         return [graph_output]


# **** Graph 3 ****
@app.callback([Output('distribucionEPS_graph','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_eps(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT 
            a.id,
            b.razon_social as EPS
            FROM Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN glb_entidads b ON a.glb_entidad_id = b.id
            WHERE EPS IS NOT NULL"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r, query=q)

            fig = graphs.graph_distribucion_eps(df)
            graph_output = [dcc.Graph(id='distribucionEPS_graph',
                                      figure=fig,
                                      config={'displaylogo': False})]

        else:
            graph_output= ['An error ocurred, please try again']

        return [graph_output]


# **** Graph 4 ****
@app.callback([Output('distribucionIPS_graph','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_ips(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT 
            a.id,
            b.razon_social as EPS
            FROM Modulo_PQR_Sector_Salud a
            LEFT OUTER JOIN glb_entidads b ON a.glb_entidad_id = b.id
            WHERE EPS IS NOT NULL"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r, query=q)

            fig = graphs.graph_distribucion_eps(df)
            graph_output = [dcc.Graph(id='distribucionIPS_graph',
                                      figure=fig,
                                      config={'displaylogo': False})]

        else:
            graph_output= ['An error ocurred, please try again']

        return [graph_output]


# **** Graph 5 ****
@app.callback([Output('distribucionSISBEN_graph','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_sisben(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT 
            ID,
            PUNTAJE as sisben
            FROM AMISALUD_TM_SISBEN_MENSUAL"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r, query=q)

            fig = graphs.graph_distribucion_sisben(df)
            graph_output = [dcc.Graph(id='distribucionIPS_graph',
                                      figure=fig,
                                      config={'displaylogo': False})]

        else:
            graph_output= ['An error ocurred, please try again']

        return [graph_output]

# **** Graph 6 ****
@app.callback([Output('distribucionSexo_graph','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_sexo(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT 
            ID,
            SEXO
            FROM AMISALUD_TM_MAESTRO_AFILIADOS"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r, query=q)

            fig = graphs.graph_distribucion_sexo(df)
            graph_output = [dcc.Graph(id='distribucionSexo_graph',
                                      figure=fig,
                                      config={'displaylogo': False})]

        else:
            graph_output= ['An error ocurred, please try again']

        return [graph_output]

# **** Graph 7 ****
@app.callback([Output('distribucionEdad_graph','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_edad(date_filter,url):

        if url == '/pqr_dashboard':

            q = """
            SELECT 
            ID,
            FECHA_NACIMIENTO
            FROM AMISALUD_TM_MAESTRO_AFILIADOS"""
            r = "./BDIBAGUE.db"
            df = model.querier(ruta_db=r, query=q)

            fig = graphs.graph_distribucion_edad(df)
            graph_output = [dcc.Graph(id='distribucionEdad_graph',
                                      figure=fig,
                                      config={'displaylogo': False})]

        else:
            graph_output= ['An error ocurred, please try again']

        return [graph_output]