import dash_bootstrap_components as dbc
import dash

#import os
from flask import Flask
#Suppress Dash server posts to console
#import logging as Flasklog
#flog = Flasklog.getLogger('werkzeug')
#flog.setLevel(Flasklog.ERROR)

# initialise the flask app and define secret_key for flask session
server = Flask(__name__)
#server.secret_key = os.urandom(16)
#log = logging.Client()

app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server,
    external_stylesheets=[
        [dbc.themes.BOOTSTRAP]
    ], external_scripts=[{'src':'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js'}])
app.title = 'PQRS Analytics'