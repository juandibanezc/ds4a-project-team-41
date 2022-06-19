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

            q = "SELECT COUNT(DISTINCT id) as peticiones FROM Modulo_PQR_Sector_Salud_Cleaned WHERE tipo_solicitud = 'Peticion'"#.format(date1=date_filter[0], date2=date_filter[1])
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/IBAGUEDB.db"
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

            q = "SELECT COUNT(DISTINCT id) as sugerencias FROM Modulo_PQR_Sector_Salud_Cleaned WHERE tipo_solicitud = 'Sugerencia'"#.format(date1=date_filter[0], date2=date_filter[1])
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/IBAGUEDB.db"
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

            q = "SELECT COUNT(DISTINCT id) as reclamos FROM Modulo_PQR_Sector_Salud_Cleaned WHERE tipo_solicitud = 'Reclamo'"#.format(date1=date_filter[0], date2=date_filter[1])
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/IBAGUEDB.db"
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

            q = "SELECT COUNT(DISTINCT id) as quejas FROM Modulo_PQR_Sector_Salud_Cleaned WHERE tipo_solicitud = 'Queja'"#.format(date1=date_filter[0], date2=date_filter[1])
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/IBAGUEDB.db"
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

            query = """   SELECT CASE glb_estado_id
                                WHEN 1 THEN "Radicado"
                                WHEN 2 THEN "Digitalizado"
                                WHEN 3 THEN "En tramite"
                                WHEN 4 THEN "Proceso cerrado"
                                WHEN 5 THEN "Resuelto"
                                WHEN 6 THEN "Documento sin resp"
                            END AS estado, fecha_radicacion FROM Modulo_PQR_Sector_Salud"""
                    #         WHERE fecha_radicacion BETWEEN {date1} AND {date2}
                    # """.format(date1=date_filter[0], date2=date_filter[1])

            q = "SELECT estado_pqr as estado, fecha_radicacion FROM Modulo_PQR_Sector_Salud_Cleaned"#.format(date1=date_filter[0], date2=date_filter[1])
            r = "/Users/juan/Documents/DS4A /Final_Project/ds4a-project-team-41/IBAGUEDB.db"

            fig = graphs.graph_seguimiento_pqrs(query=q, ruta_db=r)
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