from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def codificar_tildes(df):
    """
    Codifica las letras con tilde en los nombres de las columnas de un dataframe en su equivalente sin tilde 
    y quita las ñ de las palabras.
    
    Args:
    - df : El dataframe a modificar.
    
    Returns:
    - df: El dataframe modificado, con los nombres de sus columnas sin tildes ni ñ.
    """
    df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return df


def cambio_orden_variable(df, variable, variable_anterior):
    """
    Cambia el orden de una variable en un dataframe, colocándola inmediatamente después de otra variable específica.
    
    Args:
    - df: El dataframe a modificar.
    - variable (str): El nombre de la variable que se desea mover.
    - variable_anterior (str): El nombre de la variable que se encuentra inmediatamente antes de la variable a mover.
    
    Returns:
    - df: El dataframe modificado, con la variable movida a su nueva posición.
    """
    columnas = list(df.columns)
    columnas.remove(variable)
    columnas = columnas[:columnas.index(variable_anterior)+1] + [variable] + columnas[columnas.index(variable_anterior)+1:]
    df = df.reindex(columns=columnas)
    return df


def imputacion_reg_lineal(df, var_dependiente, var_independiente):
    """
    Imputa valores ausentes en una variable dependiente de un dataframe utilizando regresión lineal.
    
    Args:
    - df: El dataframe a modificar.
    - var_dependiente (str): El nombre de la variable dependiente con valores ausentes a imputar.
    - var_independiente (str): El nombre de la variable independiente que se utilizará para predecir los valores ausentes.
    
    Returns:
    - df: El dataframe modificado, con los valores ausentes de la variable dependiente imputados.
    """
    missings = df[df[var_dependiente].isna()]
    no_missings = df.dropna(subset=[var_dependiente])

    modelo = LinearRegression().fit(no_missings[[var_independiente]], no_missings[var_dependiente])
    prediccion = modelo.predict(missings[[var_independiente]])
    df.loc[df[var_dependiente].isna(), var_dependiente] = prediccion

    return df


def imputacion_groupby(df, columna):
    """
    Rellena los valores missings de una columna en un dataframe con la mediana de los valores no missings 
    de esa columna, agrupando por otra columna específica.
    
    Parámetros:
    -----------
    - df : Dataframe en el que se buscará la columna especificada para rellenar los valores ausentes.
    - columna : str
        Nombre de la columna que se rellenará con la mediana de sus valores no ausentes.
        
    Retorna:
    --------
    - df : El dataframe original con la columna especificada actualizada, rellenando sus valores ausentes con 
        la mediana de los valores no ausentes de esa columna, agrupando por otra columna específica.
    """
    df[columna] = df[columna].fillna(df.groupby('Codigo primario CNAE adaptado')[columna].transform('median'))
    return df



def creacion_dfs_finales(df, columnas_financieras_completas ):
        
    # CREACION DE LOS 2 DFS FINALES PARA LOS MODELOS
    # DF_ADQUISICION
    df_pivotado= df.pivot_table(index='Codigo_NIF', columns='year', values=columnas_financieras_completas,)
    df_pivotado_columnas= df_pivotado.columns
    df_pivotado_copia= df_pivotado.copy()

    # se pasan las columnas de los años de df_pivotado como sufijo de las columnas de df_pivotado
    df_pivotado.columns= df_pivotado.columns.map('{0[0]}_{0[1]}'.format)
    df_pivotado= df_pivotado.reset_index()
    # luego se añaden el resto de columnas de df seleccionando las que no estan en df_pivotado
    columnas= columnas_financieras_completas.tolist()
    df_adquisicion_completo= pd.merge(df_pivotado, df.loc[:,~df.columns.isin(columnas)], on= 'Codigo_NIF', how='left')

    # se quita 1 de cada 2 filas porque hay duplicados
    df_adquisicion_completo= df_adquisicion_completo.drop_duplicates(subset='Codigo_NIF', keep='first')

    # se crea otro df quitando las columnas de 2020
    df_adquisicion_2021= df_adquisicion_completo.drop(df_adquisicion_completo.filter(regex='_2020').columns, axis=1)

    # se calcula el ratio de crecimiento de las variables financieras entre 2020 y 2021
    df_pivotado_ratios= pd.DataFrame()
    for col in df_pivotado_columnas.get_level_values(0):
        df_pivotado_ratios[col+'_ratio']=df_pivotado_copia[col][2021]/df_pivotado_copia[col][2020]
    df_pivotado_ratios= df_pivotado_ratios.reset_index()

    # se junta el df de ratios con el df de adquisicion
    df_adquisicion_final= pd.merge(df_pivotado_ratios,df_adquisicion_2021 , on='Codigo_NIF', how='left')
    df_adquisicion_final=df_adquisicion_final.applymap(lambda x: 99999 if x== np.inf else x)
    df_adquisicion_final=df_adquisicion_final.applymap(lambda x: -99999 if x== -np.inf else x)
    df_adquisicion_final= df_adquisicion_final.fillna(0)



    # DF_VALORACION
    # Primero se crea el df que estA preparado para hacer el modelo de valoracion de empresas
    # se busca cuando valoracion no es na
    df_valoracion= df_adquisicion_final[df_adquisicion_final['valuation_2022']!=0]

    # ahora que se ha creado el df de valoracion, se quita la columna de valoracion del df de adquisicion
    df_adquisicion_final= df_adquisicion_final.drop('valuation_2022', axis=1)

    # se quita la segunda instancia de cada empresa y se queda con la del 2021
    df_valoracion= df_valoracion.drop_duplicates(subset='Codigo_NIF', keep='first')
    df_valoracion= df_valoracion.drop('year', axis=1)
    df_valoracion.shape

    # Se RalizaN estos calculos si alguna de estas columnas es nula, y se sustituye el valor nulo por el calculado
    df_valoracion.loc[:,'Precio/Venta']=(df_valoracion['valuation_2022']/df_valoracion['Importe neto Cifra de Ventas mil EUR_2021'])
    df_valoracion.loc[:,'Precio/Ebitda']=(df_valoracion['valuation_2022']/df_valoracion['EBITDA mil EUR_2021'])
    df_valoracion.loc[:,'PER']=(df_valoracion['valuation_2022']/df_valoracion['EBIT mil EUR_2021'])

    # Se reemplazan valores infinitos con valores altos.
    df_valoracion.loc[:,'Precio/Venta']=df_valoracion['Precio/Venta'].replace([np.inf, -np.inf], [99999, -99999])

    return df_adquisicion_final, df_valoracion


def seleccion_de_variables(df, variable_objetivo, variables_con_missings_antes_nif):
    correlacion = df.corr()[variable_objetivo]

    # solo se cogen los que tengan una correlacion más alta que 0.3
    df_correlacion_valor_absoluto = pd.DataFrame({'Variables': correlacion.index, f'Correlacion con {variable_objetivo}': correlacion.abs().values}).sort_values(by=f'Correlacion con {variable_objetivo}', ascending=False)

    # si la variable objetivo es valuation_2022 se cogen correlaciones mayores que 0.3 y sino mayores que 0.1
    if variable_objetivo=='valuation_2022':
        columnas_a_mantener = list(df_correlacion_valor_absoluto[df_correlacion_valor_absoluto[f'Correlacion con {variable_objetivo}'] > 0.3]['Variables'].values)
    else:
        columnas_a_mantener = list(df_correlacion_valor_absoluto[df_correlacion_valor_absoluto[f'Correlacion con {variable_objetivo}'] > 0.1]['Variables'].values)

    df_seleccionado = df[columnas_a_mantener]

    # se hace un modelo random forest para ver qué variables son las más importantes
    x = df_seleccionado.drop(variable_objetivo, axis=1)
    y = df_seleccionado[variable_objetivo]

    rf = RandomForestRegressor(random_state=0)
    rf.fit(x, y)

    forest_importances = pd.Series(rf.feature_importances_, index=x.columns).sort_values(ascending=True)

    # Crear dataframe con importancia de características
    forest_importances = forest_importances.to_frame().reset_index()
    forest_importances.columns = ['feature', 'importance']

    # cambio las terminaciones de las columnas, quitando _2021 y _ratio para tener en cuenta cuáles fueron imputadas previamente
    forest_importances['feature'] = forest_importances['feature'].str.replace('_2021', '')
    forest_importances['feature'] = forest_importances['feature'].str.replace('_ratio', '')

    variables_con_missings_antes_nif = variables_con_missings_antes_nif.reset_index()
    variables_con_missings_antes_nif.columns = ['feature', 'index']

    # merge forest_importances con variables_con_missings_antes_nif por la columna feature
    variables_con_missings_antes_nif = pd.merge(variables_con_missings_antes_nif, forest_importances, on='feature', how='right')
    variables_con_missings_antes_nif['index'] = variables_con_missings_antes_nif['index'].fillna(0)

    # se eliminan las filas (en el df_valoracion_seleccionado columnas) con más de 80 missings (index)
    variables_con_missings_antes_nif = variables_con_missings_antes_nif[variables_con_missings_antes_nif['index'] < 80]

    df_seleccionado_final = df_seleccionado.loc[:, df_seleccionado.columns.str.startswith(tuple(variables_con_missings_antes_nif['feature']))]
    df_seleccionado_final = pd.concat([df_seleccionado_final, df_seleccionado[variable_objetivo]], axis=1)

    return df_seleccionado_final