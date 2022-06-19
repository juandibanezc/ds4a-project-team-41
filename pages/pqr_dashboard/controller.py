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
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/BDIBAGUE.db"
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
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/BDIBAGUE.db"
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
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/BDIBAGUE.db"
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
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/BDIBAGUE.db"
            df = model.querier(ruta_db=r,query=q)
            kpi_output = df.loc[0,'quejas']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** Graph 1 ****
@app.callback([Output('seguimientoPQR_graph','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def Graph_1(date_filter,url):

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
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/BDIBAGUE.db"
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
# def Graph_2(date_filter,url):

#         if url == '/pqr_dashboard':

#             query = "".format(date1=date_filter[0], date2=date_filter[1])
#             df = model.querier(query)

#             graph_output = "graph function"

#         else:
#             graph_output= ['An error ocurred, please try again']

#         return [graph_output]


# # **** Graph 3 ****
# @app.callback([Output('dashboard_KPIrow3','children')],
#               [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
#                Input('url', 'pathname')])
# def Graph_3(date_filter,url):

#         if url == '/pqr_dashboard':

#             query = "".format(date1=date_filter[0], date2=date_filter[1])
#             df = model.querier(query)

#             graph_output = "graph function"

#         else:
#             graph_output= ['An error ocurred, please try again']

#         return [graph_output]


# # **** Graph 4 ****
# @app.callback([Output('dashboard_KPIrow4','children')],
#               [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
#                Input('url', 'pathname')])
# def Graph_4(date_filter,url):

#         if url == '/pqr_dashboard':

#             query = "".format(date1=date_filter[0], date2=date_filter[1])
#             df = model.querier(query)

#             graph_output = "graph function"

#         else:
#             graph_output= ['An error ocurred, please try again']

#         return [graph_output]


# # **** Graph 5 ****
# @app.callback([Output('dashboard_KPIrow5','children')],
#               [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
#                Input('url', 'pathname')])
# def Graph_5(date_filter,url):

#         if url == '/pqr_dashboard':

#             query = "".format(date1=date_filter[0], date2=date_filter[1])
#             df = model.querier(query)

#             graph_output = "graph function"

#         else:
#             graph_output= ['An error ocurred, please try again']

#         return [graph_output]

# # **** Graph 6 ****
# @app.callback([Output('dashboard_KPIrow6','children')],
#               [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
#                Input('url', 'pathname')])
# def Graph_6(date_filter,url):

#         if url == '/pqr_dashboard':

#             query = "".format(date1=date_filter[0], date2=date_filter[1])
#             df = model.querier(query)

#             graph_output = "graph function"

#         else:
#             graph_output= ['An error ocurred, please try again']

#         return [graph_output]

# # **** Graph 7 ****
# @app.callback([Output('dashboard_KPIrow7','children')],
#               [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
#                Input('url', 'pathname')])
# def Graph_7(date_filter,url):

#         if url == '/pqr_dashboard':

#             query = "".format(date1=date_filter[0], date2=date_filter[1])
#             df = model.querier(query)

#             graph_output = "graph function"

#         else:
#             graph_output= ['An error ocurred, please try again']

#         return [graph_output]