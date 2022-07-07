from dash import Input, Output, State
from base.login import view as login
from pages.pqr_dashboard import view  as pqr_dashboard
from pages.pqr_exploration import view as pqr_exploration
from pages.pqr_reports import view as pqr_reports
from app import app
import time

from flask import render_template

from app import server

from pages.config import model

@server.route('/report')
def report():
    
    q = f"""
    SELECT 
        COUNT(DISTINCT a.id) as peticiones 
    FROM 
        Modulo_PQR_Sector_Salud a
        LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
    WHERE 
        b.TIPO_PETICION IN ('Peticion')
        """
    
    df = model.querier(q)
    kpi_output = df.loc[0,'peticiones']
    
    data = {
        'report_date' : kpi_output, #r'23 de MARZO de 2022.',
        'report_period' : r'ENERO DE 2022',
        'text1' : r'Durante el mes de ENERO DE 2022, se radicaron un total de 115 PQRS, correspondientes a la Dirección de Aseguramiento.',
        'text2' : r'Durante el mes de ENERO DE 2022, se radicaron un total de 115 PQRS, de los cuales los grupos poblacionales con mayor vulneración de sus derechos en salud fueron los adultos entre los 27 a los 59 años con un 32,17% y los infantes menores de 11 años con un porcentaje de 20,86%.',
        'text3' : r'Durante el mes de ENERO DE 2022 se radicaron un total de 115 PQRS, se brindó más apoyo con un 43% a las personas de género femenino ante la vulneración de sus derechos, en el caso del género masculino se brindo un apoyo del 39%.',
        'text4' : r'Durante el mes de ENERO 2022 se radicaron un total de 115 PQRS, de los cuales el 19,13% corresponde a la comuna 1, 12,17% corresponde a la comuna 9, 8,69% corresponden a la comuna 8 de Ibagué, donde los habitantes de estas comunas fueron los que más radicaron PQRS en busca del cumplimiento de sus derechos en salud. En este periodo de tiempo la comuna 7 y la comuna 13 de Ibagué presentaron el nivel más bajo de PQRS radicados en la Dirección de Aseguramiento de la Secretaria de Salud Municipal de Ibagué ya que no realizó la radicación de ninguna queja, reclamo o sugerencia.',
        'text5' : r'Durante el mes de ENERO DE 2022 se radicaron un total de 115 PQRS, la EAPB en la que los usuarios en salud requirieron más apoyo para el cumplimiento de sus derechos fue NUEVA EPS con un 48%, seguido de MEDIMAS EPS con un 18%.',
        'text6' : r'Durante el mes de ENERO DE 2022 se radicaron un total de 115 PQRS, el tipo de PQRS que más se radicó fue la de Reclamo en un 40%, ya que para los usuarios en salud somos el puente para garantizar la prestación del servicio en salud; seguido de Peticiones con un 39%, en donde dan a conocer las posibles oportunidades a mejorar el servicio, un mal proceso o algún suceso que a su parecer deja de ser justo.',
        'text8' : r'Durante el mes de ENERO 2022 se radicaron un total de 115 PQRS, a la fecha se encuentran resueltos en el 78,26% de los casos y se encuentran en trámite en un 21,74%.'
        
    }
    return render_template('report.html', data=data)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('url','search')])
def display_page(pathname, search): 

    try:

        t1 = time.time()

        redirect = {'/': pqr_dashboard.layout,
                    '/pqr_dashboard': pqr_dashboard.layout,
                    '/pqr_exploration': pqr_exploration.layout,
                    '/pqr_reports': pqr_reports.layout,
                    # '/profile': profile.layout,
                    # '/messages': messages.layout,
                    # 'NoAccess': NoAccess.layout,
                    }

        return redirect[pathname]
    except Exception as e:
        print(f'Catched the following exception while redirecting: {e}')





