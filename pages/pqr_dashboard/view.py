from dash import html, dcc
from app import app
import dash_mantine_components as dmc
from datetime import date
import calendar

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
                                                                                html.Img(src='/assets/images/peticiones-icon.png', className="kpi-img")                                                                                
                                                                                ]),
                                                                        html.Div(children=[
                                                                                html.H4("Peticiones", className="kpi-titles"),
                                                                                html.H3(id='peticiones_count', className="kpi-counts")
                                                                        ], className="title-kpi-div")                                                      
                                                                ], className="box"),

                                                                html.Div(id="quejas_box", children=[
                                                                        html.Div(id="quejas_title", style={'float':'left', 'width':'40%'},className="", children=[
                                                                                html.Img(src='/assets/images/quejas-icon.png', className="kpi-img")                                                                                
                                                                                ]),
                                                                        html.Div(children=[
                                                                                html.H4("Quejas", className="kpi-titles"),
                                                                                html.H3(id='quejas_count', className="kpi-counts")
                                                                        ], className="title-kpi-div")                                                
                                                                ], className="box"),

                                                                html.Div(id="reclamos_box", children=[
                                                                        html.Div(id="sugerencias_title", style={'float':'left', 'width':'40%'},className="", children=[
                                                                                html.Img(src='/assets/images/reclamos-icon.png', className="kpi-img")                                                                                
                                                                                ]),
                                                                        html.Div(children=[
                                                                                html.H4("Reclamos", className="kpi-titles"),
                                                                                html.H3(id='reclamos_count', className="kpi-counts")
                                                                        ], className="title-kpi-div")                                                
                                                                ], className="box"),

                                                                html.Div(id="sugerencias_box", children=[
                                                                        html.Div(id="sugerencias_title", style={'float':'left', 'width':'40%'},className="", children=[
                                                                                html.Img(src='/assets/images/sugerencias-icon.png', className="kpi-img")                                                                                
                                                                                ]),
                                                                        html.Div(children=[
                                                                                html.H4("Sugerencias", className="kpi-titles"),
                                                                                html.H3(id='sugerencias_count', className="kpi-counts")
                                                                        ], className="title-kpi-div")                                                
                                                                ], className="box"),
                                                                
                                                        ], className='row KPI')]
                                                        ),
                          html.Br(),         
                          dcc.Loading(id='loading_dashboard_3',
                                      children=[html.Div(id="dashboard_graphRow_1",
                                                        children=[
                                                                html.Div(id="seguimientoPQR_box", children=[
                                                                        html.H4("Seguimiento de PQRS", id="seguimientoPQR_title", className="title"),
                                                                        html.Div(dcc.Graph(id='seguimientoPQR_graph'), id="seguimientoPQR", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="distribucionPQRCOMUNA_box", children=[
                                                                        html.H4("Distribución de PQRS por Comunas", id="distribucionPQRCOMUNA_title",className="title"),
                                                                        html.Div(dcc.Graph(id='distribucionPQRCOMUNA_graph'), id="distribucionPQRCOMUNA", className="graficos")
                                                                ], className='boxGraph')

                                                        ], className='row graphRow1')]),
                          html.Br(),
                          dcc.Loading(id='loading_dashboard_4',
                                      children=[html.Div(id="dashboard_graphRow_2",
                                                        children=[
                                                                html.Div(id="distribucionEPS_box", children=[
                                                                        html.H4("Distribución de PQRS por Entidad", id="", className="title"),
                                                                        html.Div(dcc.Graph(id='distribucionEPS_graph'), id="distribucionEPS", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="distribucionSISBEN_box", children=[
                                                                        html.H4("Distribución de PQRS por Grupo de Sisben", id="",className="title"),
                                                                        html.Div(dcc.Graph(id='distribucionSISBEN_graph'), id="distribucionSISBEN", className="graficos")
                                                                ], className='boxGraph')
                                                        ], className='row graphRow1')]),
                        
                        html.Br(),
                        dcc.Loading(id='loading_dashboard_5',
                                        children=[html.Div(id="dashboard_graphRow_3",
                                                        children=[
                                                                html.Div(id="", children=[
                                                                        html.H4("Distribución de PQRS por Sexo", id="",className="title"),
                                                                        html.Div(dcc.Graph(id='distribucionSexo_graph'), id="distribucionSexo", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="", children=[
                                                                        html.H4("Distribución de PQRS por Edad", id="",className="title"),
                                                                        html.Div(dcc.Graph(id='distribucionEdad_graph'), id="distribucionEdad", className="graficos")
                                                                ], className='boxGraph')

                                                        ], className='row graphRow1')]),
                        
                        html.Br(),
                        dcc.Loading(id='loading_dashboard_6',
                                        children=[html.Div(id="dashboard_graphRow_4",
                                                        children=[
                                                                html.Div(id="", children=[
                                                                        html.H4("Distribución Tipo Petición vs Comuna", id="",className="title"),
                                                                        html.Div(dcc.Graph(id='distribucionTipoComuna_graph'), id="distribucionTipoComuna", className="graficos")
                                                                ], className='boxGraph'),
                                                                html.Div(id="", children=[
                                                                        html.H4("Distribución Tipo Petición vs Entidad", id="",className="title"),
                                                                        html.Div(dcc.Graph(id='distribucionTipoEntidad_graph'), id="distribucionTipoEntidad", className="graficos")
                                                                ], className='boxGraph')

                                                        ], className='row graphRow1')]),
                   ]
)

layout = html.Div(className='container-fluid',
                              children=[  
                              html.Div(className='row',
                                        children=[
                                        html.H1(id='dashboard-title', children = 'PQRS DASHBOARD', className="col-6 page-title"),
                                        # html.Div(children=[
                                        #         dbc.Button('Generar Informe', id='informeButton', n_clicks=0, className='me-1', size='lg'),
                                        #         dbc.Modal([
                                        #                 dbc.ModalHeader(dbc.ModalTitle("Header")),
                                        #                 dbc.ModalBody("Body Content of the Modal"),
                                        #         ], id="modal-lg", size="lg", is_open=False),
                                        # ], className="col-3", style={'align-self':'center'}),
                                        html.Div(children=[
                                                html.H4('Selecciona un rango de fecha:'),
                                                html.Div(id="date-filters-div",className="",
                                                                                children= [
                                                                                  html.Div(children=[
                                                                                      dmc.DateRangePicker(
                                                                                                  id={'type':"date-range-picker","index":"pqr_dashboard"},
                                                                                                  value=[(date.today().replace(month=1).replace(day=1)).strftime('%Y-%m-%d'),(date.today().replace(month=12).replace(day=calendar.monthrange(date.today().year, 12)[1])).strftime('%Y-%m-%d')],
                                                                                                  amountOfMonths=2,
                                                                                                  dropdownType="modal",
                                                                                                  zIndex=1000,
                                                                                                  shadow='sm',
                                                                                                  modalZIndex=1000,
                                                                                                  allowSingleDateInRange = True,
                                                                                                  
                                                                                      )
                                                                                  ])
                                                                        ])
                                                  ], className="date_filter"),
                                                ]),
                                        html.Div(id='div-dashboard-MainContainer',
                                                children=content)])



