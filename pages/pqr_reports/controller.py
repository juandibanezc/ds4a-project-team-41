from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_extensions.snippets import send_file
import dash
from app import app
from pages.pqr_reports import model
import sys, os


import jinja2
import pdfkit

# **** Report Generation ****

@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def func(n_clicks):
    return send_file('./report_out.pdf', mime_type='application/pdf')


@app.callback([Output('report-generation-alert','children')],
              #Output("download", "data"),
              [Input('report-button', "n_clicks"),
               State({'type':"date-range-picker","index":"pqr_reports"}, "value"),
               State('url', 'pathname')], prevent_initial_call=True)
def generacion_reporte(btn, date_filter, url):

        if url == '/pqr_reports':

          try:
            
            #text_21, text_22 = model.report_2(date_filter)
            #text_31, text_32 = model.report_3(date_filter)
            #text_41, text_42 = model.report_4(date_filter)
            #text_51, text_52 = model.report_5(date_filter)
            #text_61, text_62 = model.report_6(date_filter)
            #text_81, text_82 = model.report_8(date_filter)
            #print(text_81,text_82)

            # Jinja2 function
            
            templateLoader = jinja2.FileSystemLoader(searchpath="./templates/")
            templateEnv = jinja2.Environment(loader=templateLoader)
            TEMPLATE_FILE = "report.html"
            template = templateEnv.get_template(TEMPLATE_FILE)
            
            data = {
                'report_date' : r'23 de MARZO de 2022.',
                'text1' : r'Durante el mes de ENERO DE 2022, se radicaron un total de 115 PQRS, correspondientes a la Dirección de Aseguramiento.',
                'text21' : r'Se realiza la caracterización de la población que según la radicación de PQRS se le han vulnerado sus derechos en salud, con el fin de identificar qué grupo etario es más vulnerable.',
                'text22' : r'Durante el mes de ENERO DE 2022, se radicaron un total de 115 PQRS, de los cuales los grupos poblacionales con mayor vulneración de sus derechos en salud fueron los adultos entre los 27 a los 59 años con un 32,17% y los infantes menores de 11 años con un porcentaje de 20,86%.',
                'text31' : r'Se realiza la caracterización de la población que según la radicación de PQRS fueron radicadas durante el mes de ENERO DE 2022, identificando el género de mayor vulnerabilidad.',
                'text32' : r'Durante el mes de ENERO DE 2022 se radicaron un total de 115 PQRS, se brindó más apoyo con un 43% a las personas de género femenino ante la vulneración de sus derechos, en el caso del género masculino se brindo un apoyo del 39%.',
                'text41' : r'Se realiza la caracterización de la población que según la radicación de PQRS del mes de ENERO 2022 se le han vulnerado sus derechos o sus requerimientos en salud, con esto podemos identificar qué comuna requiere apoyo.',
                'text42' : r'Durante el mes de ENERO 2022 se radicaron un total de 115 PQRS, de los cuales el 19,13% corresponde a la comuna 1, 12,17% corresponde a la comuna 9, 8,69% corresponden a la comuna 8 de Ibagué, donde los habitantes de estas comunas fueron los que más radicaron PQRS en busca del cumplimiento de sus derechos en salud. En este periodo de tiempo la comuna 7 y la comuna 13 de Ibagué presentaron el nivel más bajo de PQRS radicados en la Dirección de Aseguramiento de la Secretaria de Salud Municipal de Ibagué ya que no realizó la radicación de ninguna queja, reclamo o sugerencia.',
                'text51' : r'El total de PQRS radicados durante el mes de ENERO 2021, en relación con la EAPB implícita en el proceso de gestión, así se realizará la evaluación por entidad identificando cuál de estas requiere mayor vigilancia y control.',
                'text52' : r'Durante el mes de ENERO DE 2022 se radicaron un total de 115 PQRS, la EAPB en la que los usuarios en salud requirieron más apoyo para el cumplimiento de sus derechos fue NUEVA EPS con un 48%, seguido de MEDIMAS EPS con un 18%.',
                'text61' : r'El total de PQRS radicados en relación con su tipo, radicados durante el mes de ENERO DE 2022.',
                'text62' : r'Durante el mes de ENERO DE 2022 se radicaron un total de 115 PQRS, el tipo de PQRS que más se radicó fue la de Reclamo en un 40%, ya que para los usuarios en salud somos el puente para garantizar la prestación del servicio en salud; seguido de Peticiones con un 39%, en donde dan a conocer las posibles oportunidades a mejorar el servicio, un mal proceso o algún suceso que a su parecer deja de ser justo.',
                'text81' : r'Analizar la cantidad de PQRS que a la fecha se encuentran resueltos radicados durante el mes de ENERO DE 2022, y que nos permita así analizar la oportunidad de gestión.',
                'text82' : r'Durante el mes de ENERO 2022 se radicaron un total de 115 PQRS, a la fecha se encuentran resueltos en el 78,26% de los casos y se encuentran en trámite en un 21,74%.'
            }
            
            outputText = template.render(data=data)
            
            pdfkit.from_string(outputText, './report_out.pdf')
            
            return [outputText]
            #return [send_file('./report_out.pdf', mime_type='application/pdf')]

          except Exception as e:
            print(e)
            return [dbc.Alert(f'There was an error during the report generation process: {e}', is_open=True, color='danger')]
            #return None
          
        else:
            return None
            #return None