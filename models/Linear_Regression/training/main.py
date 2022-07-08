# Training


# Import Libraries
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from patsy import dmatrices
from statsmodels.stats.diagnostic import het_white
import psycopg2
from dotenv import load_dotenv
import pandas.io.sql as sqlio
import os

def OLStrain(fechai, fechaf): 
    '''
    Train a OLS model using historic PQRS data between fechai and fechaf
    The arguments (fechai and fecha) are STRINGS with the format '%Y-%m-%d', for example: 2022-01-25
    '''
    # =============================================================================
    # Read data from database
    # =============================================================================
     
    query = f'''SELECT TO_DATE(fecha_radicacion, 'DD/MM/YYYY' ) AS fecha_radicacion,
                 glb_dependencia_id,
                 pqr_tipo_derechos_id,
                 ase_tipo_poblacion_id,
                 glb_entidad_id,
                 TO_DATE(fecha_vencimiento, 'DD/MM/YYYY' ) AS fecha_vencimiento,
                 TO_DATE(fecha_respuesta, 'DD/MM/YYYY' ) AS fecha_respuesta
                FROM modulo_pqr_sector_salud 
                WHERE TO_DATE(fecha_radicacion, 'DD/MM/YYYY') > TO_DATE('{fechai}', 'YYYY-MM-DD')
                AND TO_DATE(fecha_radicacion, 'DD/MM/YYYY') < TO_DATE('{fechaf}', 'YYYY-MM-DD')
                ORDER BY TO_DATE(fecha_radicacion, 'DD/MM/YYYY' )
                '''
    print(f'Reading data from database between {fechai} and {fechaf}')
    df_model = querier(query) 
    
    # =============================================================================
    # Data Cleaning and pre-processing
    # =============================================================================
    print('************************')
    print('Cleaning the data...')
    print('************************')
    
    # Drop the rows where there are nan.
    df_model = df_model.dropna()
    
    # Create columns with days between "fecha_radicado" and "fecha_respuesta"
    df_model['tiempo_respuesta'] = (df_model.fecha_respuesta - df_model.fecha_radicacion).dt.days # This may be possible to do in the Query
    
    # Delete data where tiempo_respuesta is negative (corrupte data)
    df_model = df_model[df_model.tiempo_respuesta>=0] # This can be done in the Query
    
    # Create a column of category for plazo where:
    # plazo < 100: 0
    # plazo between 100 and 180: 1
    # plazo > 180: 2
    df_model['plazo_categoria'] = (df_model.fecha_vencimiento - df_model.fecha_radicacion).dt.days.apply(lambda x: 0 if x <100 else 1 if (x>100) & (x <180) else 2 )
    
    # Drop 'fecha' columns. They are no longer needed
    df_model.drop(['fecha_radicacion','fecha_respuesta','fecha_vencimiento'], axis=1, inplace =True)
    
    # Assign data type (dtype) for each column
    df_model = df_model.astype({ 
    
        'glb_dependencia_id': 'category',
        'pqr_tipo_derechos_id': 'category',
        'ase_tipo_poblacion_id': 'category',
        'glb_entidad_id': 'category',
        'plazo_categoria': 'category'
    })
    
    # Delete unused categories:
    df_model[df_model.select_dtypes(include='category').columns] = df_model.select_dtypes(include='category').apply(lambda x: x.cat.remove_unused_categories(), axis=0)
    
    
    # =============================================================================
    # Train the model
    # =============================================================================
    print('************************')
    print('Traning the model...')
    print('************************')
    
    # Define train and test datasets (80% - 20%)
    train = df_model.sample(frac=0.8)  
    test = df_model.drop(train.index).sample(frac=1.0)
    
    
    # List of dependent variables
    col_list = list(train.columns)
    col_list.remove('tiempo_respuesta')
    
    # list with the variables for the OLS formula (apply C(var) syntax for categorical variables)
    col_list_all = ['C(%s)'%(x) for x in col_list ]
    
    # Fit the OLS Linear Regression model using statsmodel library
    model_plazo_log_noplazo_nosol, formula = apply_reg(col_list_all, df = train, trans='sqrt')
    
    # Apply White Test to verify heteroscedasticity in the model
    y, X = dmatrices(formula, train, return_type='dataframe')
    results = het_white(model_plazo_log_noplazo_nosol.resid, X)
    
    print('******************************')
    print('Results from White Test to detect potential heteroscedasticity:')
    print(f'  - F-Statistic for White Test is {results[1]}' )
    print(f'  - p-value for White Test is {results[2]}' )
    if results[2] < 0.05:
        print('With an alpha of 0.05 the null hypothesisis rejected so there is potential heteroscedasticity in the dataset')
    else:
        print('With an alpha of 0.05 we can not reject the null hypothesisis, so there is not proof of significant heteroscedasticity in the dataset')
    
    
    # Error Metrics for train and test datasets
    eval_df = pd.DataFrame()
    for df in ['train','test']:
        
        true_values =eval(df).tiempo_respuesta # True Values
        prediction = model_plazo_log_noplazo_nosol.predict(eval(df))**2 # Predicted values
        
        # Calculate metrics
        MAE = np.mean(np.abs(prediction-true_values))
        RMSE = np.sqrt(np.mean(np.square(prediction-true_values)))
        MAPE = np.mean(np.abs((prediction-true_values)/true_values)*100)
        # save the results in a pandas column
        eval_serie = pd.Series({'MAE':MAE,'RMSE':RMSE,'MAPE':MAPE})
        # Built a DataFrame with results for train and test
        eval_df[df] = eval_serie
    
    print('*********************************')
    print('*********************************')
    print('Error Metrics Results for train and tests datasets:')
    print(eval_df)
        
    
    # Save the model to a pickle file
    model_plazo_log_noplazo_nosol.save('LR_model_trained_%s_%s.pickle'%(fechai, fechaf))
 

# Functions to apply the OLS model to a df
def apply_reg(lista, df, trans='no'):
    
    '''
    Create a OLS model with the vars in "lista" and the data in "df"
    Arguments:    
        lista: list with the dependent variables to be included in the ols smf.formula (with format C(var) for categorical variables)
        df: dataframe that contains the independent and the dependent variables. 
        trans: 'log' or 'sqrt' if the independen variable will be transformed in the model to log(var) or sqrt(var). Otherwise, apply no transformation
    
    Returns:
        model_fit: the statsmodel object containing the result of the Linear Regression model
        formula: string with the formula used in the linear regression
    '''
    
    columns_str = " + ".join(lista)
    
    # Create the model and print its summary
    if trans == 'log':
        formula = 'np.log(tiempo_respuesta+1) ~ ' + columns_str 
    elif trans == 'sqrt':
        formula = 'np.sqrt(tiempo_respuesta) ~ ' + columns_str 
    else:
        formula = 'tiempo_respuesta ~ ' + columns_str 
    model = smf.ols(formula = formula, data = df)
    model_fit = model.fit()
    
    print('*********************************')
    print('The OLS formula is: %s'%formula)
    print('*********************************')
    print(model_fit.summary()) 
    print('*********************************')
    print('AIC from model_all is ' + str(int(model_fit.aic))); # print AIC value
    
    return model_fit, formula


def querier(transaccion):
    
    load_dotenv()
    
    DB_NAME = os.getenv('DB_NAME') 
    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PSW = os.getenv('DB_PSW')
    DB_PORT = os.getenv('DB_PORT')
    
    conn=psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PSW, port=DB_PORT,connect_timeout=300)
    cursor=conn.cursor()
     
    data = sqlio.read_sql_query(transaccion, conn)
    conn.close()

    return data



                
                

