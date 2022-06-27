from dash import Input, Output
from dash.exceptions import PreventUpdate
from app import app
from pages.config import model, graphs

# @app.callback(Output("modal-lg", "is_open"),
#               Input("informeButton", "n_clicks"),
#               State("modal-lg", "is_open"))
# def toggle_modal(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open

# **** KPI 1 ****
@app.callback([Output('peticiones_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_1(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              COUNT(DISTINCT a.id) as peticiones 
            FROM 
              Modulo_PQR_Sector_Salud a
              LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE 
              b.TIPO_PETICION IN ('Peticion')
              AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""
            
            df = model.querier(q)
            kpi_output = df.loc[0,'peticiones']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** KPI 2 ****
@app.callback([Output('sugerencias_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_2(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              COUNT(DISTINCT a.id) as sugerencias 
            FROM 
              Modulo_PQR_Sector_Salud a
              LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE 
              b.TIPO_PETICION IN ('Solicitud')
              AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""
            
            df = model.querier(q)
            kpi_output = df.loc[0,'sugerencias']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** KPI 3 ****
@app.callback([Output('reclamos_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_3(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              COUNT(DISTINCT a.id) as reclamos 
            FROM 
              Modulo_PQR_Sector_Salud a
              LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE 
              b.TIPO_PETICION IN ('Reclamo')
              AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            kpi_output = df.loc[0,'reclamos']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# **** KPI 4 ****
@app.callback([Output('quejas_count','children')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def KPI_4(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              COUNT(DISTINCT a.id) as quejas 
            FROM 
              Modulo_PQR_Sector_Salud a
              LEFT OUTER JOIN tipo_peticion b ON a.pqr_tipo_solicitud_id = b.ID
            WHERE 
              b.TIPO_PETICION IN ('Queja','Denuncia')
              AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            kpi_output = df.loc[0,'quejas']

        else:
            kpi_output= ['An error ocurred, please try again']

        return [kpi_output]

# # **** Graph 1 ****
@app.callback([Output('seguimientoPQR_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def seguimiento_pqrs(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              CASE b.descripcion 
              WHEN 'Radicado' THEN 'En Tramite'
              WHEN 'Digitalizado' THEN 'En Tramite'
              WHEN 'En Tramite' THEN 'En Tramite'
              WHEN 'Proceso cerrado' THEN 'Resuelto'
              WHEN 'Resuelto' THEN 'Resuelto'
              WHEN 'Documentos sin respuesta' THEN 'Resuelto' END as estado, 
              to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') as fecha_radicacion 
            FROM 
              Modulo_PQR_Sector_Salud a
              LEFT OUTER JOIN glb_estados b ON CAST(a.glb_estado_id AS varchar) = CAST(b.id AS varchar)
            WHERE 
              to_char(to_date(a.fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            fig = graphs.graph_seguimiento_pqrs(df)

        else:
            raise PreventUpdate
        
        return [fig]

# # **** Graph 2 ****
@app.callback([Output('distribucionPQRCOMUNA_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def mapa_comunas(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              glb_comunas_corregimientos.descripcion as id, 
              COUNT(Modulo_PQR_Sector_Salud.id) as cantidad 
            FROM 
              Modulo_PQR_Sector_Salud 
              LEFT OUTER JOIN glb_barrios_veredas ON CAST(Modulo_PQR_Sector_Salud.glb_barrio_vereda_id AS varchar) = CAST(glb_barrios_veredas.id AS varchar) 
              LEFT OUTER JOIN glb_comunas_corregimientos ON CAST(glb_barrios_veredas.glb_comunas_corregimiento_id AS varchar) = CAST(glb_comunas_corregimientos.id AS varchar) 
              LEFT OUTER JOIN tipo_peticion ON CAST(Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_id AS varchar) = CAST(tipo_peticion.ID AS varchar)
            WHERE 
              glb_comunas_corregimientos.descripcion LIKE 'Comuna %'
              AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'
            GROUP BY 
              glb_comunas_corregimientos.descripcion
            """

            df = model.querier(q)
            fig = graphs.graph_mapa_comunas(df)
            
        else:
            raise PreventUpdate

        return [fig]


# **** Graph 3 ****
@app.callback([Output('distribucionEPS_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_entidad(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              a.id,
              b.razon_social as entidad
            FROM 
              Modulo_PQR_Sector_Salud a
              LEFT OUTER JOIN glb_entidads b ON CAST(a.glb_entidad_id AS varchar) = CAST(b.id AS varchar)
            WHERE 
              b.razon_social IS NOT NULL
              AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            fig = graphs.graph_distribucion_entidad(df)

        else:
            raise PreventUpdate

        return [fig]


# **** Graph 4 ****
@app.callback([Output('distribucionSISBEN_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_sisben(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              a.identificacion,
              a.puntaje as grupo
            FROM 
              AMISALUD_TM_SISBEN_MENSUAL a
              --JOIN Modulo_PQR_Sector_Salud b
              --ON CAST(a.identificacion AS varchar) = CAST(b.identificacion AS varchar)
            --WHERE
              --AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            fig = graphs.graph_distribucion_sisben(df)
            
        else:
            raise PreventUpdate

        return [fig]

# **** Graph 5 ****
@app.callback([Output('distribucionSexo_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_sexo(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              a.identificacion,
              a.sexo
            FROM 
              AMISALUD_TM_MAESTRO_AFILIADOS a
              --JOIN Modulo_PQR_Sector_Salud b
              --ON CAST(a.identificacion AS varchar) = CAST(b.identificacion AS varchar)
            --WHERE
              --AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            fig = graphs.graph_distribucion_sexo(df)

        else:
            raise PreventUpdate

        return [fig]

# **** Graph 6 ****
@app.callback([Output('distribucionEdad_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_edad(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
            ID,
            FECHA_NACIMIENTO
            FROM AMISALUD_TM_MAESTRO_AFILIADOS
            --WHERE
              --AND to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            fig = graphs.graph_distribucion_edad(df)

        else:
            raise PreventUpdate

        return [fig]


# **** Graph 7 ****
@app.callback([Output('distribucionTipoComuna_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_tipo_peticion_comuna(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              tipo_peticion.TIPO_PETICION as tipo_peticion, 
              glb_comunas_corregimientos.descripcion 
            FROM 
              Modulo_PQR_Sector_Salud 
              JOIN glb_barrios_veredas 
              ON CAST(Modulo_PQR_Sector_Salud.glb_barrio_vereda_id AS varchar)= CAST(glb_barrios_veredas.id AS varchar) 
              JOIN glb_comunas_corregimientos 
              ON CAST(glb_barrios_veredas.glb_comunas_corregimiento_id AS varchar)= CAST(glb_comunas_corregimientos.id AS varchar) 
              JOIN tipo_peticion 
              ON CAST(Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_id AS varchar)= CAST(tipo_peticion.ID AS varchar)
            WHERE
              to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            fig = graphs.graph_distribucion_tipo_peticion_comuna(df)


        else:
            raise PreventUpdate

        return [fig]


# **** Graph 8 ****
@app.callback([Output('distribucionTipoEntidad_graph','figure')],
              [Input({'type':"date-range-picker","index":"pqr_dashboard"}, "value"),
               Input('url', 'pathname')])
def graph_distribucion_tipo_peticion_entidad(date_filter,url):

        if url == '/pqr_dashboard':

            q = f"""
            SELECT 
              tipo_peticion.TIPO_PETICION as tipo_peticion, 
              glb_entidads.razon_social as entidad
            FROM 
              Modulo_PQR_Sector_Salud 
              JOIN glb_entidads 
              ON CAST(Modulo_PQR_Sector_Salud.glb_entidad_id AS varchar) = CAST(glb_entidads.id AS varchar)
              JOIN tipo_peticion 
              ON CAST(Modulo_PQR_Sector_Salud.pqr_tipo_solicitud_id AS varchar) = CAST(tipo_peticion.ID AS varchar)
            WHERE
              to_char(to_date(fecha_radicacion, 'dd/mm/yyyy'), 'yyyy-mm-dd') BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"""

            df = model.querier(q)
            fig = graphs.graph_distribucion_tipo_peticion_entidad(df)

        else:
            raise PreventUpdate

        return [fig]