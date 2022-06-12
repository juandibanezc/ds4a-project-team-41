from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import routes

from base.side_nav import controller
from base.header_navbar import controller
from pages.pqr_dashboard import controller
from pages.pqr_exploration import controller
from pages.pqr_reports import controller
from pages.profile import controller
from pages.messages import controller


from base.side_nav import view as side_nav
from base.header_navbar import view as header_navbar
from app import app
#LOGIN
from base.login import controller
import requests

#server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
                    id = 'sidebar-menu',
                    className='sidebar',
                    children=[
                        html.Img(src='/assets/images/logo-alcaldia.png', style={'width':'80%', 'padding':'10% 0% 10% 0%'}),
                        html.A('',href='/pqr_dashboard',className='button-base home'),
                        html.A('',href='/pqr_reports',className='button-base informes'),
                        html.A('',href='/pqr_exploration',className='button-base pqr'),
                        
                    ]),

                html.Div(
                    id = 'content-layout',
                    className= 'light',
                    children=[
                        html.Div(id='page-content'),    
                    ]
                )
])

if __name__ == '__main__':
    app.run_server(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 8082)))