from turtle import width
from dash import html, dcc, Input, Output, State
from app import app
import dash_mantine_components as dmc
from datetime import date
import calendar
import dash_bootstrap_components as dbc
from dash_extensions import Download

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
                dbc.Button("Generar Informe", id="report-button", color="success", className="me-1"),
                dcc.Loading(html.Div(id="report-generation-alert")),
                html.Div([Download(id="download")])
            ], style={'width':'40%', 'float':'left'}),                
            ],style={'padding':'1% 3%', 'background-color':'white', 'margin-top':'25px', 'border':'solid 1px #6c757d', 'border-radius':'5px', 'display':'flex'})

        



layout = html.Div(className='container-fluid',
                              children=[  
                              html.Div(className='row',
                                        children=[
                                        html.H1(id='dashboard-title', children = 'GENERAR INFORME', className="col-6 page-title"),
                                                ]),
                                        html.Div(id='div-dashboard-MainContainer',
                                                children=content)])

