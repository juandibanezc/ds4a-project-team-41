from turtle import width
import click
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from pages.config import model, graphs

content = html.Div(children=[
                          dcc.Loading(id='loading_dashboard_1',
                                      type="graph",
                                      fullscreen=True,
                                      children=[dcc.Store(id='dashboard_dataStore')]),

                          html.Br(),
                          dcc.Loading(id='loading_dashboard_2',
                                      children=[html.Div(id="dashboard_KPIrow",
                                                        children=[
                                                                html.Div(id="peticiones_box", children=[
                                                                        html.Div(id="peticiones_title", style={'float':'left', 'width':'40%'},className="", children=[
                                                                                html.Img(src='/assets/images/peticiones-icon.png', style={'width':'50pt', 'padding':'0%'})                                                                                
                                                                                ]),
                                                                        html.Div(style={'float':'right','width':'60%','padding':' 1% 0 1%'}, children=[
                                                                                html.H4("Peticiones", style={'fontWeight':'bold', 'font-size':'1.5vw'}),
                                                                                html.H3("15", id='peticiones_count', style={'fontWeight':'bold','text-align': 'center', 'font-size':'1.5vw'})
                                                                        ])                                                      
                                                                ], className="box"),

                                                                html.Div(id="sugerencias_box", children=[
                                                                        html.Div(id="sugerencias_title", style={'float':'left', 'width':'40%'},className="", children=[
                                                                                html.Img(src='/assets/images/sugerencias-icon.png', style={'width':'50pt', 'padding':'0%'})                                                                                
                                                                                ]),
                                                                        html.Div(style={'float':'right','width':'60%','padding':' 1% 0 1%'}, children=[
                                                                                html.H4("Sugerencias", style={'fontWeight':'bold', 'font-size':'1.5vw'}),
                                                                                html.H3("15", id='sugerencias_count', style={'fontWeight':'bold','text-align': 'center', 'font-size':'1.5vw'})
                                                                        ])                                                
                                                                ], className="box"),

                                                                html.Div(id="reclamos_box", children=[
                                                                        html.Div(id="sugerencias_title", style={'float':'left', 'width':'40%'},className="", children=[
                                                                                html.Img(src='/assets/images/reclamos-icon.png', style={'width':'50pt', 'padding':'0%'})                                                                                
                                                                                ]),
                                                                        html.Div(style={'float':'right','width':'60%','padding':' 1% 0 1%'}, children=[
                                                                                html.H4("Reclamos", style={'fontWeight':'bold', 'font-size':'1.5vw'}),
                                                                                html.H3("15", id='reclamos_count', style={'fontWeight':'bold','text-align': 'center', 'font-size':'1.5vw'})
                                                                        ])                                                
                                                                ], className="box"),
                                                                
                                                                html.Div(id="quejas_box", children=[
                                                                        html.Div(id="quejas_title", style={'float':'left', 'width':'40%'},className="", children=[
                                                                                html.Img(src='/assets/images/quejas-icon.png', style={'width':'50pt', 'padding':'0%'})                                                                                
                                                                                ]),
                                                                        html.Div(style={'float':'right','width':'60%','padding':' 1% 0 1%'}, children=[
                                                                                html.H4("Quejas", style={'fontWeight':'bold', 'font-size':'1.5vw'}),
                                                                                html.H3("15", id='quejas_count', style={'fontWeight':'bold','text-align': 'center', 'font-size':'1.5vw'})
                                                                        ])                                                
                                                                ], className="box"),
                                                        ], className='row KPI')]
                                                        ),
                          html.Br(),         
                          dcc.Loading(id='loading_dashboard_3',
                                      children=[html.Div(id="dashboard_graphRow_1",
                                                        children=[
                                                                html.Div(id="seguimientoPQR_box", children=[
                                                                        html.H4("Seguimiento de PQRs", id="seguimientoPQR_title", className="title"),
                                                                        html.Div("GRAFICO DE SEGUMIENTO DE PQRS", id="seguimientoPQR_graph", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="distribucionPQRCOMUNA_box", children=[
                                                                        html.H4("Distribución de PQRs por Comunas", id="distribucionPQRCOMUNA_title",className="title"),
                                                                        html.Div("GRAFICO DE DISTRIBUCIÓN DE PQRS POR COMUNAS", id="distribucionPQRCOMUNA_graph", className="graficos")
                                                                ], className='boxGraph')

                                                        ], className='row graphRow1')]),
                          html.Br(),
                          dcc.Loading(id='loading_dashboard_4',
                                      children=[html.Div(id="dashboard_graphRow_2",
                                                        children=[
                                                                html.Div(id="distribucionEPS_box", children=[
                                                                        html.H4("Distribución por EPS", id="", className="title"),
                                                                        html.Div("GRAFICO DE DISTRIBUCIÓN POR EPS", id="distribucionEPS_graph", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="distribucionSISBEN_box", children=[
                                                                        html.H4("Distribución por SISBEN", id="",className="title"),
                                                                        html.Div("GRAFICO DE DISTRIBUCIÓN POR SISBEN", id="distribucionSISBEN_graph", className="graficos")
                                                                ], className='boxGraph')
                                                        ], className='row graphRow1')]),
                        html.Br(),
                        dcc.Loading(id='loading_dashboard_5',
                                        children=[html.Div(id="dashboard_graphRow_3",
                                                        children=[
                                                                html.Div(id="", children=[
                                                                        html.H4("Tipo de PQR vs EPS", id="", className="title"),
                                                                        html.Div("GRAFICO DE PQR VS EPS", id="PQRVSEPS_graph", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="", children=[
                                                                        html.H4("Tipo de PQR vs COMUNAS", id="",className="title"),
                                                                        html.Div("GRAFICO DE PQR VS COMUNAS", id="PQRVSCOMUNAS_graph", className="graficos")
                                                                ], className='boxGraph')

                                                        ], className='row graphRow1')]),
                        html.Br(),
                        dcc.Loading(id='loading_dashboard_6',
                                        children=[html.Div(id="dashboard_graphRow_4",
                                                        children=[
                                                                html.Div(id="", children=[
                                                                        html.H4("OTRO GRAFICO", id="",className="title"),
                                                                        html.Div("OTRO GRAFICO", id="distribucionIPS_graph", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="", children=[
                                                                        html.H4("OTRO GRAFICO", id="",className="title"),
                                                                        html.Div("OTRO GRAFICO", id="PQRVSCOMUNAS_graph", className="graficos")
                                                                ], className='boxGraph')

                                                        ], className='row graphRow1')]),
                   ]
)

layout = html.Div(className='container-fluid',
                              children=[  
                              html.Div(className='row',
                                        children=[
                                        html.H1(id='dashboard-title', children = 'PQR Dashboard', className="col-3", style={'float':'left','font-weight': 'bolder', 'font-size': 'xxx-large'}),
                                        html.Div(children=[
                                                dbc.Button('Generar Informe', id='informeButton', n_clicks=0, className='me-1', size='lg'),
                                                dbc.Modal([
                                                        dbc.ModalHeader(dbc.ModalTitle("Header")),
                                                        dbc.ModalBody("Body Content of the Modal"),
                                                ], id="modal-lg", size="lg", is_open=False),
                                        ], className="col-3", style={'align-self':'center'}),
                                        html.Div(children=[
                                                html.H4('Selecciona un rango de fecha:', style={'padding-right':'5%'}),
                                                html.Div(id="date-filters-div",className="", style={"width":"50%", 'float':'right', 'padding':'1% 5% 1% 5%'},
                                                                                children=graphs.dateFilter(id="pqr_dashboard"))

                                        ], style={'float':'right', 'width':'50%', 'text-align':'right'}),
                                       
                                        
                                      ]),
                              html.Div(id='div-dashboard-MainContainer',
                                       children=content)])


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

app.callback(
    Output("modal-lg", "is_open"),
    Input("informeButton", "n_clicks"),
    State("modal-lg", "is_open"),
)(toggle_modal)