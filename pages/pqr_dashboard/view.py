from dash import html, dcc
import dash_bootstrap_components as dbc

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
                                                                        html.Div(id="peticiones_title", className="custom-grid1", children=[
                                                                                html.Img(src='/assets/images/peticiones-icon.png', style={'width':'70%', 'padding':'0%'}),
                                                                                html.H6("Peticiones", style={'margin':'0', 'padding':'0 1% 0 1%', 'fontWeight':'bold'})
                                                                                ]),
                                                                        html.Div(id="peticiones_data_box", className="custom-grid2", children=[
                                                                                html.H3("15", id='peticiones_count', style={'margin':'0', 'padding':'0 1% 0 5%', 'fontWeight':'bold'}),
                                                                                html.Div("GRAFICO PETICIONES", id="peticiones_graph", style={'margin':'0', 'padding':'0 1% 0 1%', 'width':'100%'})
                                                                                ])                                                        
                                                                ], className="box"),
                                                                html.Div(id="sugerencias_box", children=[
                                                                        html.Div(id="sugerencias_title", className="custom-grid1", children=[
                                                                                html.Img(src='/assets/images/sugerencias-icon.png', style={'width':'70%', 'padding':'0%'}),
                                                                                html.H6("Sugerencias", style={'margin':'0', 'padding':'0 1% 0 1%', 'fontWeight':'bold'})
                                                                                ]),
                                                                        html.Div(id="sugerencias_data_box", className="custom-grid2", children=[
                                                                                html.H3("10", id='sugerencias_count', style={'margin':'0', 'padding':'0 1% 0 5%', 'fontWeight':'bold'}),
                                                                                html.Div("GRAFICO SUGERENCIAS", id="sugerencias_graph", style={'margin':'0', 'padding':'0 1% 0 1%', 'width':'100%'})
                                                                                ])                                                        
                                                                ], className="box"),
                                                                html.Div(id="reclamos_box", children=[
                                                                        html.Div(id="reclamos_title", className="custom-grid1", children=[
                                                                                html.Img(src='/assets/images/reclamos-icon.png', style={'width':'70%', 'padding':'0%'}),
                                                                                html.H6("Reclamos", style={'margin':'0', 'padding':'0 1% 0 1%', 'fontWeight':'bold'})
                                                                                ]),
                                                                        html.Div(id="reclamos_data_box", className="custom-grid2", children=[
                                                                                html.H3("20", id='reclamos_count', style={'margin':'0', 'padding':'0 1% 0 5%', 'fontWeight':'bold'}),
                                                                                html.Div("GRAFICO RECLAMOS", id="reclamos_graph", style={'margin':'0', 'padding':'0 1% 0 1%', 'width':'100%'})
                                                                                ])                                                        
                                                                ], className="box"),
                                                                html.Div(id="quejas_box", children=[
                                                                        html.Div(id="quejass_title", className="custom-grid1", children=[
                                                                                html.Img(src='/assets/images/quejas-icon.png', style={'width':'70%', 'padding':'0%'}),
                                                                                html.H6("Quejas", style={'margin':'0', 'padding':'0 1% 0 1%', 'fontWeight':'bold'})
                                                                                ]),
                                                                        html.Div(id="quejas_data_box", className="custom-grid2", children=[
                                                                                html.H3("15", id='quejas_count', style={'margin':'0', 'padding':'0 1% 0 5%', 'fontWeight':'bold'}),
                                                                                html.Div("GRAFICO QUEJAS", id="quejas_graph", style={'margin':'0', 'padding':'0 1% 0 1%', 'width':'100%'})
                                                                                ])                                                           
                                                                ], className="box")
                                                        ], className='row KPI')]
                                                        ),
                          html.Br(),         
                          dcc.Loading(id='loading_dashboard_3',
                                      children=[html.Div(id="dashboard_graphRow_1",
                                                        children=[
                                                                html.Div(id="seguimientoPQR_box", children=[
                                                                        html.H4("Seguimiento de PQRs", id="seguimientoPQR_title"),
                                                                        html.Div("GRAFICO DE SEGUMIENTO DE PQRS", id="seguimientoPQR_graph", className="graficos")
                                                                ], className='box'),
                                                                html.Div(id="distribucionPQRCOMUNA_box", children=[
                                                                        html.H4("Distribución de PQRs por Comunas", id="distribucionPQRCOMUNA_title"),
                                                                        html.Div("GRAFICO DE DISTRIBUCIÓN DE PQRS POR COMUNAS", id="distribucionPQRCOMUNA_graph", className="graficos")
                                                                ], className='box')

                                                        ], className='row graphRow1')]),
                          html.Br(),
                          dcc.Loading(id='loading_dashboard_4',
                                      children=[html.Div(id="dashboard_graphRow2",
                                      className='row'
                                   )]),
                          dcc.Loading(id='loading_dashboard_5',
                                      children=[html.Div(id="dashboard_graphRow3",
                                      className='row'
                                          )]),
                   ]
)

layout = html.Div(className='container-fluid',
                              children=[  
                              html.Div(className='row',
                                      children=[
                                      html.H1(id='dashboard-title', children = 'PQR Dashboard', className="fw-bold col-12 col-md-6")
                                      # html.Div(id="date-filters-div",className="row col-12 col-md-6 p-0", style={"width":"40%"},children=
                                      #               DVGraph.DateFilters(id="commercial_dashboard")
                                      ]),
                              html.Div(id='div-dashboard-MainContainer',
                                       children=content)])