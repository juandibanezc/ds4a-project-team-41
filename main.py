from turtle import color, position
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import routes
from dash import Input, Output, State

from base.side_nav import controller
from base.header_navbar import controller
from pages.pqr_dashboard import controller
from pages.pqr_exploration import controller
from pages.pqr_reports import controller


from base.side_nav import view as side_nav
from base.header_navbar import view as header_navbar
from app import app
#LOGIN
from base.login import controller
import requests
import pdfkit

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
                    id = 'sidebar-menu',
                    className='sidebar',
                    children=[
                        html.Img(className="logo_alcaldia", src='/assets/images/logo-alcaldia.png'),
                        html.Div(children=[
                            html.A(children=[
                                html.Img(src='/assets/images/dashboard.png', className='button-base', alt="Dashboard"),
                                html.Div(children=[html.H4('DASHBOARD', style={'color':'white', 'font-weight':'bolder', 'margin':'0%'})], className="option")
                            ],href='/pqr_dashboard')
                        ],style={'padding':'5% 0%','position':'relative'}),
                        html.Div(children=[
                            html.A(children=[ 
                                html.Img(src='/assets/images/informes.png',className='button-base'),
                                html.Div(children=[html.H4('GENERAR INFORME', style={'color':'white', 'font-weight':'bolder', 'margin':'0%'})], className="option")
                            ],href='/pqr_reports')
                        ],style={'padding':'5% 0%','position':'relative'}),
                        html.Div(children=[
                            html.A(children=[ 
                                html.Img(src='/assets/images/pqr.png',className='button-base'),
                                html.Div(children=[html.H4('MÓDULO DE ANÁLISIS', style={'color':'white', 'font-weight':'bolder', 'margin':'0%'})], className="option")
                            ],href='/pqr_exploration')
                        ],style={'padding':'5% 0%','position':'relative'}),
                    ]),

                html.Div(
                    id = 'content-layout',
                    className= 'light',
                    children=[
                        html.Div(id='page-content'),    
                    ]
                )
])

#region MODAL
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open


app.callback(
    Output("modal-lg", "is_open"),
    [Input("open-lg", "n_clicks"), Input("close-dismiss", "n_clicks")],
    State("modal-lg", "is_open"),
)(toggle_modal)
#endregion MODAL

#region PDF Generator

#endregion 
if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 8080)))