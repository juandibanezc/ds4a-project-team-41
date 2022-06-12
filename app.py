#from google.cloud import logging
#import jwt
from dash.exceptions import PreventUpdate
import dash

import os
#from flask import Flask
#Suppress Dash server posts to console
import logging as Flasklog
#flog = Flasklog.getLogger('werkzeug')
#flog.setLevel(Flasklog.ERROR)

# initialise the flask app and define secret_key for flask session
#server = Flask(__name__)
#server.secret_key = os.urandom(16)
#log = logging.Client()

app = dash.Dash(__name__, #suppress_callback_exceptions=True, #  server=server,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css"
    ])
app.title = 'PQR Analytics'