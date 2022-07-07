from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash
from app import app
from pages.pqr_reports import model
import sys, os

# **** Report Generation ****
@app.callback([Output('report-generation-alert','children')],
              [Input('report-button', "n_clicks"),
               State({'type':"date-range-picker","index":"pqr_reports"}, "value"),
               State('url', 'pathname')], prevent_initial_call=True)
def generacion_reporte(btn, date_filter, url):

        if url == '/pqr_reports':

          try:
            
            text_21, text_22 = model.report_2(date_filter)
            text_31, text_32 = model.report_3(date_filter)
            text_41, text_42 = model.report_4(date_filter)
            text_51, text_52 = model.report_5(date_filter)
            text_61, text_62 = model.report_6(date_filter)
            text_81, text_82 = model.report_8(date_filter)
            print(text_81,text_82)

            # Jinja2 function
            output = ['Finished']


          except Exception as e:
            print(e)
            output = [dbc.Alert(f'There was an error during the report generation process: {e}',
                                    is_open=True,
                                    color='danger')]
          
        else:
            output= ['An error ocurred, please try again']

        return [output]