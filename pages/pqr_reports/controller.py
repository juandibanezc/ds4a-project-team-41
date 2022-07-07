from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_extensions.snippets import send_file
import dash
from app import app
from pages.pqr_reports import model
import sys, os
from flask import request

import jinja2
import pdfkit

@app.callback([Output("download", "data"), Output('report-generation-alert','children')],
              [Input('report-button', "n_clicks"),
               State({'type':"date-range-picker","index":"pqr_reports"}, "value"),
               State('url', 'pathname')], prevent_initial_call=True)
def generacion_reporte(btn, date_filter, url):

        if url == '/pqr_reports':

          try:
            
            text_21, text_22 = model.report_2(date_filter)
            #text_31, text_32 = model.report_3(date_filter)
            text_41, text_42 = model.report_4(date_filter)
            text_51, text_52 = model.report_5(date_filter)
            text_61, text_62 = model.report_6(date_filter)
            text_81, text_82 = model.report_8(date_filter)
            #print(text_81,text_82)

            # Jinja2 function
            
            templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
            templateEnv = jinja2.Environment(loader=templateLoader)
            TEMPLATE_FILE = "report.html"
            template = templateEnv.get_template(TEMPLATE_FILE)
            
            data = {
                'host_url': request.host_url,
                'text1' : 'TODO',
                'text21' : text_21, 'text22' : text_22,
                'text31' : 'TODO', 'text32' : 'TODO',
                'text41' : text_41, 'text42' : text_42,
                'text51' : text_51, 'text52' : text_52,
                'text61' : text_61, 'text62' : text_62,
                'text81' : text_81, 'text82' : text_82
            }
            
            outputText = template.render(data=data)
            
            #return [outputText]
            
            pdfkit.from_string(outputText, './report_out.pdf')
            
            return [send_file('./report_out.pdf', mime_type='application/pdf'), dbc.Alert('Informe generado con éxito!', is_open=True, color='success')]

          except Exception as e:
            print(e)
            return [None, dbc.Alert(f'There was an error during the report generation process: {e}', is_open=True, color='danger')]  
                  
        else:
            return None