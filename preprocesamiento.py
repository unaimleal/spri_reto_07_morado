import pandas as pd
import numpy as np
import os

CARPETA_DATOS_ORIGINALES = 'Datos/Originales/'
df_sabi_1= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_modif_1.xlsx'))
df_sabi_2= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_modif_2.xlsx'))
df_dealroom= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_dealroom_modif.xlsx'))

# pasamos el n.s. a NaN con applymap
df_sabi_2=df_sabi_2.applymap(lambda x: np.nan if x=='n.s.' else x)

# creamos columna con numero de missing por fila
df_sabi_2['n_missings']= df_sabi_2.isna().sum(axis=1)

# sacamos el codigo_nif de las empresas que tienen mas de 20 missings
empresas_missings= df_sabi_2[df_sabi_2['n_missings']>20]['Codigo_NIF'].unique()

# eliminamos las empresas con mas de 20 missings en df_sabi_2 y despues en df_sabi_1 y df_dealroom
df_sabi_2= df_sabi_2[~df_sabi_2['Codigo_NIF'].isin(empresas_missings)]
df_sabi_1= df_sabi_1[~df_sabi_1['Codigo_NIF'].isin(empresas_missings)]
df_dealroom= df_dealroom[~df_dealroom['Codigo_NIF'].isin(empresas_missings)]

# Convertimos la primera letra de cada palabra a mayuscula 
columnas= ['last_funding_date', 'first_funding_date']
for i in columnas:
    df_dealroom[i]= df_dealroom[i].str.title()
# hay tres valores de fecha que aparece solo el año, lo pasamos a formato mes/año
for i in columnas:
    for ano in ['2021', '2003', '2017']:
        try:
            indice = df_dealroom[df_dealroom[i]==ano].index[0]
            df_dealroom.at[indice, i] = f'Jan/{ano}'
        except IndexError:
            pass
# pasamos las fechas a datetime
df_dealroom['last_funding_date']= pd.to_datetime(df_dealroom['last_funding_date'], format='%b/%Y')
df_dealroom['first_funding_date']= pd.to_datetime(df_dealroom['first_funding_date'], format='%b/%Y')

# pasamos b2b a 1 en una columna, b2c a 1 en otra, y dejamos los que son ambos a 0
df_dealroom['b2b']= df_dealroom['b2b_b2c'].apply(lambda x: 1 if x=='business' else 0)
df_dealroom['b2c']= df_dealroom['b2b_b2c'].apply(lambda x: 1 if x=='consumer' else 0)


# UNION DE LOS DF
# juntamos los dos df_sabi
df_sabi= pd.merge(df_sabi_1, df_sabi_2, on='Codigo_NIF', how='inner')
# juntamos este df con el de dealroom
df= pd.merge(df_sabi, df_dealroom, on='Codigo_NIF', how='inner')

# MÁS MODIFICACIONES
# hay 10 valores que no hay en la columna de sabi, pero si en la de dealroom, por lo que los pasamos
df['Número empleados']= df['Número empleados'].fillna(df['n_empleados_dealroom'])

# quitamos la columna de n_empleados_dealroom
df= df.drop('n_empleados_dealroom', axis=1)

# Pasamos a formato datetime 
df['Fecha constitucion']=pd.to_datetime(df['Fecha constitucion'], format='%Y/%m/%d')
df['last_funding_date']=pd.to_datetime(df['last_funding_date'], format='%Y/%m/%d')

#creamos una variable para conocer los años que lleva la empresa en el mercado
df['Años en Mercado']= (2023-df['Fecha constitucion'].dt.year)
columnas = list(df.columns)
columnas.remove('Años en Mercado')
# alteramos el orden de las columnas para que los años en el mercado vayan despues de la fecha de constitucion
columnas = columnas[:columnas.index("Fecha constitucion")+1] + ['Años en Mercado'] + columnas[columnas.index("Fecha constitucion")+1:]
df = df.reindex(columns=columnas)

#creamos una variable para conocer los años desde que se realizón la última financiación.
df['Años desde ultima finanziacion']= (2023-df['last_funding_date'].dt.year).fillna(0).astype(int)

columnas = list(df.columns)
columnas.remove('Años desde ultima finanziacion')
columnas = columnas[:columnas.index('last_funding_date')+1] + ['Años desde ultima finanziacion'] + columnas[columnas.index('last_funding_date')+1:]
df = df.reindex(columns=columnas)