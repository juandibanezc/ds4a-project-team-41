# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from tkinter import font
from tkinter.ttk import Style
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from vistas import dashboard, informes, pqrs

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
                dcc.Location(id='url', refresh=False),
                html.Div(
                    id = 'sidebar-menu',
                    className='sidebar',
                    children=[
                        html.Img(src='/assets/images/logo-alcaldia.png', style={'width':'80%', 'padding':'10% 0% 10% 0%'}),
                        html.A('',href='http://127.0.0.1:8050/dashboard',className='button-base home'),
                        html.A('',href='http://127.0.0.1:8050/informes',className='button-base informes'),
                        html.A('',href='http://127.0.0.1:8050/pqr',className='button-base pqr'),
                        
                    ]),

                html.Div(
                    id = 'content-layout',
                    className= 'light',
                    children=[
                        html.Div(id='page-content'),    
                    ]
                )
            ])

@callback(Output('page-content', 'children'),
            Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/informes':
        return informes.layout
    elif pathname == '/pqr':
        return pqrs.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)