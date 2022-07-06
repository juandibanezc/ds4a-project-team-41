from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
from app import app
from pages.pqr_exploration.model import OLSprediction
from pages.config.model import querier

# **** Dynamic Fields ****
@app.callback([Output('tipo-derecho', "options"),
               Output('tipo-poblacion', "options"),
               Output('dependencia', "options"),
               Output('entidad', "options")],
              [Input('url', 'pathname')])
def populate_fields(url):

        if url == '/pqr_exploration':

          output = []
          q = f'''SELECT 
                    CAST(pqr_tipo_derechos_id AS INTEGER) AS tipo_derechos,
                    b.descripcion AS tipo_derechos_desc,
                    CAST(ase_tipo_poblacion_id AS INTEGER) AS tipo_poblacion,
                    c.descripcion AS tipo_poblacion_desc,
                    CAST(glb_dependencia_id AS INTEGER) AS dependencia,
                    glb_dependencia_id AS dependencia_desc,
                    CAST(glb_entidad_id AS INTEGER) AS entidad,
                    d.razon_social AS entidad_desc
                  FROM 
                    modulo_pqr_sector_salud a
                    JOIN pqr_tipo_derechos b ON CAST(a.pqr_tipo_derechos_id AS varchar) = CAST(b.id AS varchar)
                    JOIN ase_tipo_poblacions c ON CAST(a.ase_tipo_poblacion_id AS varchar) = CAST(c.id AS varchar)
                    JOIN glb_entidads d ON CAST(a.glb_entidad_id AS varchar) = CAST(d.id AS varchar)
                  GROUP BY 
                    dependencia,
                    dependencia_desc, 
                    tipo_derechos,
                    tipo_derechos_desc,
                    tipo_poblacion,
                    tipo_poblacion_desc,
                    entidad,
                    entidad_desc
                  '''

          df = querier(q)
          for col in df.columns:
            if 'desc' not in col:
                options = [{"label": f"{row[1]}. {row[0].split('. ')[-1]}", "value": row[1]} for col_, row in df[[col+'_desc',col]].drop_duplicates().iterrows()]
                output.append(options)   

        else:
            raise PreventUpdate

        return output

# **** Multiple Regression Model 1 ****
@app.callback([Output('resultado-estimacion1','children')],
              [Input('boton-estimacion1', "n_clicks"),
               State('input-estimacion1', "value"),
               State('url', 'pathname')], prevent_initial_call=True)
def prediccion_tiempo_respuesta_1(btn,id, url):

        if url == '/pqr_exploration':

            prediction = OLSprediction(int(id),'assets/pkl/LR_model_BEST_prection.pickle')

        else:
            prediction= ['An error ocurred, please try again']

        return [prediction]

# **** Multiple Regression Model 2 ****
@app.callback([Output('resultado-estimacion2','children')],
              [Input('boton-estimacion2', "n_clicks"),
               State('tipo-derecho', "value"),
               State('tipo-poblacion', "value"),
               State('dependencia', "value"),
               State('entidad', "value"),
               #State('fecha-radicacion', "value"),
               #State('fecha-vencimiento', "value"),
               State('url', 'pathname')], prevent_initial_call=True)
def prediccion_tiempo_respuesta_2(*args):

        ctx = dash.callback_context
        url = ctx.states['url.pathname']

        if url == '/pqr_exploration':

          inputs = {}
          inputs['pqr_tipo_derechos_id'] = [int(ctx.states['tipo-derecho.value'])] 
          inputs['ase_tipo_poblacion_id'] = [int(ctx.states['tipo-poblacion.value'])] 
          inputs['glb_dependencia_id'] = [int(ctx.states['dependencia.value'])] 
          inputs['glb_entidad_id'] = [int(ctx.states['entidad.value'])] 
          inputs['fecha_radicacion'] = ['2022-01-25']#[ctx.states['fecha-radicacion.value']] 
          inputs['fecha_vencimiento'] = ['2022-06-24']#[ctx.states['fecha-vencimiento.value']] 

          prediction = OLSprediction(inputs,'assets/pkl/LR_model_BEST_prection.pickle')

        else:
            prediction= ['An error ocurred, please try again']

        return [prediction]