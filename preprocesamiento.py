import pandas as pd
import numpy as np
import os

CARPETA_DATOS_ORIGINALES = 'Datos/Originales/'
df_sabi_1= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_modif_1.xlsx'))
df_sabi_2= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_modif_2_new.xlsx'))
df_dealroom= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_dealroom_modif.xlsx'))
df_sabi_3= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_parte3.xlsx'))

# de df_sabi_3 nos quedamos solo con 4 variables
df_sabi_3_final= df_sabi_3[['Codigo_NIF','year', 'Gastos de personal mil EUR', 'Coste medio de los empleados mil']]

# pasamos el n.s. a NaN con applymap
df_sabi_2=df_sabi_2.applymap(lambda x: np.nan if x=='n.s.' else x)
df_sabi_3=df_sabi_3.applymap(lambda x: np.nan if x=='n.s.' else x)

# se crea una columna con numero de missing por fila
df_sabi_2['n_missings']= df_sabi_2.isna().sum(axis=1)

# se sustituyen las letras con tildes por las letras sin tildes de todas las columnas de df_sabi_2
# pasar funcion a otro script
def codificar_tildes(df):   
    df.columns= df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return df
df_sabi_2= codificar_tildes(df_sabi_2)
# lo mismo con el resto de dataframes
df_sabi_1= codificar_tildes(df_sabi_1)
df_dealroom= codificar_tildes(df_dealroom)
df_sabi_3_final= codificar_tildes(df_sabi_3_final)

# guardamos las columnas financieras
columnas_financieras= df_sabi_2.columns 
columnas_financieras= columnas_financieras.append(df_sabi_3_final.columns)


# TRANSFORMACIONES DE VARIABLES
# se pasa el growth stage a dummy
mapping = {'seed': 0, 'early growth': 1, 'late growth': 2}
df_dealroom['growth_stage'] = df_dealroom['growth_stage'].map(mapping)



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

# se busca si es b2b o b2c a mano y se crea una funcion para automatizarlo
lista_empresa_consumer= ['Feelfree Rentals', 'Modfie', 'Worldpats', 'Kimet Sport', 'Puntodis', 'DNA Data' ]
lista_empresa_bussines= ['Hub Gasteiz', 'Quevedos Strategic Partners', 'Anbiolab', 'Solid Machine Vision', 'Innovative Hall Media Technologies', 'lorke systems',
'Gistek Insurance Solutions', 'VIRTUALWARE', 'Naivan', ]
for empresa in lista_empresa_consumer:
    df_dealroom.iloc[df_dealroom[df_dealroom['name_dealroom'] == empresa].index[0],13]= 'consumer'
for empresa in lista_empresa_bussines:
    df_dealroom.iloc[df_dealroom[df_dealroom['name_dealroom'] == empresa].index[0],13]= 'business'

# pasamos b2b a 1 en una columna, b2c a 1 en otra, y dejamos los que son ambos a 0
df_dealroom['b2b']= df_dealroom['b2b_b2c'].apply(lambda x: 1 if x=='business' else 0)
df_dealroom['b2c']= df_dealroom['b2b_b2c'].apply(lambda x: 1 if x=='consumer' else 0)


# UNION DE LOS DF
# se juntan los tres df_sabi
df_sabi= pd.merge(df_sabi_1, df_sabi_2, on='Codigo_NIF', how='inner')
df_sabi_completo= pd.merge(df_sabi, df_sabi_3_final, on=['Codigo_NIF','year'], how='left')
# juntamos este df con el de dealroom
df= pd.merge(df_sabi_completo, df_dealroom, on='Codigo_NIF', how='inner')

# MÁS MODIFICACIONES
# hay 10 valores que no hay en la columna de sabi, pero si en la de dealroom, por lo que los pasamos
df['Numero empleados']= df.loc[:,'Numero empleados'].fillna(df['n_empleados_dealroom'])

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

# seguir en otras cosas a hacer