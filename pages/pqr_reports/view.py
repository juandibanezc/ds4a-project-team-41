from turtle import width
from dash import html, dcc, Input, Output, State
from app import app
import dash_mantine_components as dmc
from datetime import date
import calendar
import dash_bootstrap_components as dbc

content = html.Div(children=[
            html.Div([
                dbc.Label("Seleccione un rango de fecha: ", className="mr-2"),
                dmc.DateRangePicker(
                                    id={'type':"date-range-picker","index":"pqr_reports"},
                                    value=[(date.today().replace(month=1).replace(day=1)).strftime('%Y-%m-%d'),(date.today().replace(month=12).replace(day=calendar.monthrange(date.today().year, 12)[1])).strftime('%Y-%m-%d')],
                                    amountOfMonths=2,
                                    dropdownType="modal",
                                    zIndex=1000,
                                    shadow='sm',
                                    modalZIndex=1000,
                                    allowSingleDateInRange = True,
                                    style={'width':'80%'}
                                ),
                html.Br(),
                dbc.Button("Descargar Informe", id="report-button", color="success", className="me-1"),
                dcc.Loading(html.Div(id="report-generation-alert"))
            ], style={'width':'40%', 'float':'left'}),
            html.Div([
                dbc.Label("Seleccione los Gráficos que desea incluir en el informe: ", className="mr-2"),
                html.Br(),
                dbc.Checklist(
                    options=[
                        {"label": "Seguimiento de PQRs ", "value": 1},
                        {"label": "Distribución de PQRs por Comunas", "value": 2},
                        {"label": "Distribución de PQRs por Entidad", "value": 3},
                        {"label": "Distribución de PQRS por Grupo de Sisben", "value": 4},
                        {"label": "Distribución de PQRS por Sexo", "value": 5},
                        {"label": "Distribución de PQRS por Edad", "value": 6},
                        {"label": "Distribución Tipo Petición vs Comuna", "value": 7},
                        {"label": "Distribución Tipo Petición vs Entidad", "value": 8},


                    ],
                    value=[1],
                    id="checklist-input",
                ),
    
            ], style={'width':'60%', 'float':'right'}),
                
            ],style={'padding':'1% 3%', 'background-color':'white', 'margin-top':'25px', 'border':'solid 1px #6c757d', 'border-radius':'5px', 'display':'flex'})

        



layout = html.Div(className='container-fluid',
                              children=[  
                              html.Div(className='row',
                                        children=[
                                        html.H1(id='dashboard-title', children = 'GENERAR INFORME', className="col-6 page-title"),
                                                ]),
                                        html.Div(id='div-dashboard-MainContainer',
                                                children=content)])

