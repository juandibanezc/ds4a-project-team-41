# =============================================================================
# Multiple Regression Model Prediction
# =============================================================================

# Import Libraries
import pandas as pd
import statsmodels.api as sm
import psycopg2
from dotenv import load_dotenv
import pandas.io.sql as sqlio
from pages.config.model import querier
import os

def OLSprediction(inputs, model_file_path):

    '''
    This function apply an OLS model to a set of variables from a PQR in order to predict the number of days it will take to answer the PQRS
    Inputs:
        
        - inputs: an integer with the ID of the PQRS to be predicted or a list with the values of the variables that describes the PQRS.
            
            If a dict, the variables required are: 
            - pqr_tipo_derechos_id (int)
            - ase_tipo_poblacion_id (int)
            - glb_dependencia_id (int)
            - glb_entidad_id (int)
            - fecha_radicacion (str in format YYYY-mm-dd)
            - fecha_vencimiento (str in format YYYY-mm-dd)
            
            If an integer, the ID provided should identify a PQRS with valid values for all the forementioned variables. Otherwise, the model won't work
        
        - model_file: string with the path and name of the pickle file that contains the trained model that will be applied. 
    
    Output:
    Returns a DataFrame with the inputs of the model and with the estimated prediction in the column 'tiempo_respuesta_predicho'
    '''
    
    if type(inputs) == int: # If the input is an ID of a PQRS, we should read the data for that ID in the DB
              
        query = f'''SELECT TO_DATE(fecha_radicacion, 'DD/MM/YYYY' ) AS fecha_radicacion,
             CAST(glb_dependencia_id AS INTEGER),
             CAST(pqr_tipo_derechos_id AS INTEGER),
             CAST(ase_tipo_poblacion_id AS INTEGER),
             CAST(glb_entidad_id AS INTEGER),
             TO_DATE(fecha_vencimiento, 'DD/MM/YYYY' ) AS fecha_vencimiento
            FROM modulo_pqr_sector_salud 
            WHERE CAST(ID AS INTEGER) = {str(inputs)}
            '''
        print(f'Reading data from database for ID {str(inputs)}')
        df_model = querier(query) 
        
        
    elif type(inputs) == dict:  # if the input is a list of elements with the values for each variable
            variables = ['pqr_tipo_derechos_id',
                        'ase_tipo_poblacion_id',
                        'glb_dependencia_id',
                        'glb_entidad_id',               
                        'fecha_radicacion',
                        'fecha_vencimiento']
            
            df_model= pd.DataFrame(data=inputs)#, columns = variables)
            df_model['fecha_radicacion'] = pd.to_datetime(df_model['fecha_radicacion'])
            df_model['fecha_vencimiento'] = pd.to_datetime(df_model['fecha_vencimiento'])

    if df_model.glb_dependencia_id[0] == 134:
        raise ValueError('The model does not work for dependencia_id = 134 because these PQRS do not have valid values for all the other required variables')
    # =============================================================================
    # Data Cleaning and pre-processing
    # =============================================================================
    print('*****************')
    print('Data Cleaning...')
    print('*****************')
    
 
    # Create a column of category for plazo where:
    # plazo < 100: 0
    # plazo between 100 and 180: 1
    # plazo = 180: 2
    df_model['plazo_categoria'] = (df_model.fecha_vencimiento - df_model.fecha_radicacion).dt.days.apply(lambda x: 0 if x <100 else 1 if (x>100) & (x <180) else 2 )
    
    # Assign data type (dtype) for each column
    df_model = df_model.astype({ 
    
        'glb_dependencia_id': 'category',
        'pqr_tipo_derechos_id': 'category',
        'ase_tipo_poblacion_id': 'category',
        'glb_entidad_id': 'category',
        'plazo_categoria': 'category'
    })
    
    
    # =============================================================================
    # Predict
    # =============================================================================

    # Load the model
    print('Loading the model...')
    print('********************')
    ols_model = sm.load(model_file_path)

    # Apply the model to the input data to calculate predicted values for each PQRS in df_model   
    print('Calculating the predictes values')
    print('********************')
    prediction = ols_model.predict(df_model).round(1)
    
    # Build dataframe with the input data and the prediction
    df_model['tiempo_respuesta_predicho'] = prediction
    
    # Print inputs and prediction of the model
    print('Inputs of the model:')
    for column in df_model.columns:
        if column != 'tiempo_respuesta_predicho':
            print('%s: %s'%(column, str(df_model[column].values[0])))

        else:  
            if df_model.tiempo_respuesta_predicho.isna()[0]:
                print("The model couldn't predict the desired variable")
                print('Remember that for the model to work, valid values must be entered for each variable.')
            else:
                print('---------------------------------------------')
                print('The result of the model (the days expected for the answer to the PQRS) is:')
                print('%s= %s days'%(column, str(df_model[column].values[0])))

    return  str(df_model['tiempo_respuesta_predicho'].values[0]) 