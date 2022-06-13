from dash import html, dcc
import dash_bootstrap_components as dbc

from pages.config import model, graphs

content = html.Div(children=[
                          dcc.Loading(id='loading_dashboard_1',
                                      type="graph",
                                      fullscreen=True,
                                      children=[dcc.Store(id='dashboard_dataStore')]),

                          html.Br(),
                          dcc.Loading(id='lloading_dashboard_2',
                                      children=[html.Div(id="dashboard_KPIrow",
                                                         className='row')]
                                                        ),
                          html.Br(),         
                          dcc.Loading(id='loading_dashboard_3',
                                      children=[html.Div(id="dashboard_graphRow_1",
                                      className='row'
                                   )]),
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
                                      html.H1(id='dashboard-title', children = 'PQR Dashboard', className="col-12 col-md-6"),
                                      html.Div(id="date-filters-div",className="row col-12 col-md-6 p-0", style={"width":"40%"},children=
                                                    graphs.dateFilter(id="pqr_dashboard"))
                                      ]),
                              html.Div(id='div-dashboard-MainContainer',
                                       children=content)])