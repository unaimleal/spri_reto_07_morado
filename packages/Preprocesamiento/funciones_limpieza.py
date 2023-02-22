from sklearn.linear_model import LinearRegression

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
    Imputa valores faltantes en una variable dependiente de un dataframe utilizando regresión lineal.
    
    Args:
    - df: El dataframe a modificar.
    - var_dependiente (str): El nombre de la variable dependiente con valores faltantes a imputar.
    - var_independiente (str): El nombre de la variable independiente que se utilizará para predecir los valores faltantes.
    
    Returns:
    - df: El dataframe modificado, con los valores faltantes de la variable dependiente imputados.
    """
    missings = df[df[var_dependiente].isna()]
    no_missings = df.dropna(subset=[var_dependiente])

    modelo = LinearRegression().fit(no_missings[[var_independiente]], no_missings[var_dependiente])
    prediccion = modelo.predict(missings[[var_independiente]])
    df.loc[df[var_dependiente].isna(), var_dependiente] = prediccion

    return df
