from turtle import width
from dash import html, dcc, Input, Output, State
from app import app
import dash_mantine_components as dmc
from datetime import date
import calendar
import dash_bootstrap_components as dbc

estimacion_opcion1 = dbc.Card(
    dbc.CardBody(
        [
            html.P("Ingrese el ID de la PQR a estimar: (solo números)", className="card-text"),
            dbc.Input(id="input-estimacion1", type="number", style={'width':'30%'}),
            html.Br(),
            dbc.Button("Calcular Estimación", id="boton-estimacion1"),
            html.Br(),
            dbc.Label("Cantidad de Días en que se espera dar respuesta a la PQRs a partir de la fecha de radicación: ", className="mr-2"),
            dbc.Label("12", id="resultado-estimacion1", style={'font-weight':'bolder', 'font-size':'20pt'}),
        ]
    ),
    className="mt-3",
)

estimacion_opcion2 = dbc.Card(
    dbc.CardBody(
        [
            dbc.Label("ID Tipo de Derechos:", className="mr-2"),
            dbc.Input(id="",type="number", style={'width':'30%'}),
            html.Br(),
            dbc.Label("ID Tipo de Población:", className="mr-2"),
            dbc.Select(id="tipo-poblacion",options=[
                {"label": "Poblacion 1", "value": "1"},
                {"label": "Poblacion 2", "value": "2"},
                {"label": "Poblacion 3", "value": "3"},
            ], style={'width':'30%'}),
            html.Br(),
            dbc.Label("ID Dependencia:", className="mr-2"),
            dbc.Select(id="dependencia",options=[
                {"label": "Dependencia 1", "value": "1"},
                {"label": "Dependencia 2", "value": "2"},
                {"label": "Dependencia 3", "value": "3"},
            ], style={'width':'30%'}),
            html.Br(),
            dbc.Label("ID Entidad", className="mr-2"),
            dbc.Select(id="entidad",options=[
                {"label": "Entidad 1", "value": "1"},
                {"label": "Entidad 2", "value": "2"},
                {"label": "Entidad 3", "value": "3"},
            ], style={'width':'30%'}),
            html.Br(),
            dbc.Label("Fecha de Radicación:", className="mr-2"),
            dcc.DatePickerSingle(id='fecha_radicacion', min_date_allowed=date(1995, 1, 1), initial_visible_month=date(2022, 7, 7)),
            html.Br(),html.Br(),
            dbc.Label("Fecha de Vencimiento:", className="mr-2"),
            dcc.DatePickerSingle(id='fecha_vencimiento', min_date_allowed=date(1995, 1, 1), initial_visible_month=date(2022, 7, 7)),
            html.Br(),html.Br(),
            dbc.Button("Calcular Estimación", id="boton-estimacion2"),
            html.Br(),
            dbc.Label("Cantidad de Días en que se espera dar respuesta a la PQRs a partir de la fecha de radicación: ", className="mr-2"),
            dbc.Label("12", id="resultado-estimacion2", style={'font-weight':'bolder', 'font-size':'20pt'}),
        ]
    ),
    className="mt-3",
)

content = html.Div(children=[
                          dcc.Loading(id='loading_dashboard_1',
                                      type="graph",
                                      fullscreen=True,
                                      children=[dcc.Store(id='dashboard_dataStore')]),
                          html.Br(),
                          dcc.Loading(id='modelos-accordion',
                                        children=[
                                            html.Div(
                                                dbc.Accordion(
                                                    [
                                                        dbc.AccordionItem(
                                                            [
                                                                html.P("En esta sección podrá ingresar el asunto  de su PQR para conocer a qué tipo de solicitud hace referencia."),
                                                                dbc.Textarea(className="mb-3", id="asunto-clasificacion", style={'min-height':'200px'}, placeholder="Comience a escribir el asunto de la PQR aqui."),
                                                                dbc.Button("Obtener Clasificación", id="boton-clasificacion"),
                                                                html.Br(),
                                                                dbc.Label("El asunto de PQR ingresado es de tipo:", className="mr-2"),
                                                                dbc.Label("AFILIACIÓN", id="resultado-clasificacion", style={'font-weight':'bolder', 'font-size':'20pt'}),
                                                            ],
                                                            title="1. Módulo de Clasificación de PQRs",
                                                        ),
                                                        dbc.AccordionItem(
                                                            [
                                                                html.P("En esta sección, debe seleccionar el tipo de dato de entrada de la PQR para determinar por medio de Regresión Lineal el tiempo estimado que tomará resolver la PQR."),
                                                                dbc.Tabs(
                                                                            [
                                                                                dbc.Tab(estimacion_opcion1, label="ID PQR"),
                                                                                dbc.Tab(estimacion_opcion2, label="Otras Opciones"),
                                                                            ]
                                                                        ),
                                                            ],
                                                            title="2. Estimación de Tiempo de Respuesta a la PQR",
                                                        )
                                                    ], start_collapsed=True,
                                                )
                                            )
                                        ])      
        ]
)



layout = html.Div(className='container-fluid',
                              children=[  
                              html.Div(className='row',
                                        children=[
                                        html.H1(id='dashboard-title', children = 'MÓDULO DE ANÁLISIS DE PQRS', className="col-6 page-title"),
                                                ]),
                                        html.Div(id='div-dashboard-MainContainer',
                                                children=content)])

