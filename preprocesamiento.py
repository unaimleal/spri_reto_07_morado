import pandas as pd
import numpy as np
import os
import packages.Preprocesamiento.funciones_limpieza as funciones_limpieza
import warnings
warnings.filterwarnings('ignore')

CARPETA_DATOS_ORIGINALES = 'Datos/Originales/'
df_sabi_1= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_modif_1.xlsx'))
df_sabi_2= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_modif_2_new.xlsx'))
df_dealroom= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_dealroom_modif.xlsx'))
df_sabi_3= pd.read_excel(os.path.join(CARPETA_DATOS_ORIGINALES, 'df_sabi_parte3.xlsx'))

# de df_sabi_3 nos quedamos solo con 4 variables
df_sabi_3_final= df_sabi_3[['Codigo_NIF','year', 'Gastos de personal mil EUR', 'Coste medio de los empleados mil']]

# pasamos el n.s. a NaN con applymap
df_sabi_2=df_sabi_2.applymap(lambda x: np.nan if x=='n.s.' else x)
df_sabi_3_final=df_sabi_3_final.applymap(lambda x: np.nan if x=='n.s.' else x)

# se crea una columna con numero de missing por fila
df_sabi_2['n_missings']= df_sabi_2.isna().sum(axis=1)

# se sustituyen las letras con tildes por las letras sin tildes de todas las columnas de df_sabi_2

df_sabi_2= funciones_limpieza.codificar_tildes(df_sabi_2)
# lo mismo con el resto de dataframes
df_sabi_1= funciones_limpieza.codificar_tildes(df_sabi_1)
df_dealroom= funciones_limpieza.codificar_tildes(df_dealroom)
df_sabi_3_final= funciones_limpieza.codificar_tildes(df_sabi_3_final)

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
# Se pasa a formato datetime 
df['Fecha constitucion']=pd.to_datetime(df['Fecha constitucion'], format='%Y/%m/%d')
df['last_funding_date']=pd.to_datetime(df['last_funding_date'], format='%Y/%m/%d')

# cuando el total_funding es 0, el last_funding tambii©n lo imputamos como 0
df.loc[df['total_funding']==0, 'last_funding']=0


# CREACION DE VARIABLES
#creamos una variable para conocer los años que lleva la empresa en el mercado
df['Anos en Mercado']= (2023-df['Fecha constitucion'].dt.year)
df['Anos desde ultima finanziacion']= (2023-df['last_funding_date'].dt.year).fillna(0).astype(int)
df['ratio_last_funding']=df['last_funding']/df['total_funding']
df['startup']= df['Anos en Mercado'].apply(lambda x: 1 if x<7 else 0)

# se crea una variable dummy para saber si la empresa es una sociedad anonima o no
df['Sociedad_anonima']= df['Forma juridica'].apply(lambda x: 1 if 'Sociedad anonima' in x else 0)

# se utiliza funcion para cambiar el orden de las columnas creadas
df= funciones_limpieza.cambio_orden_variable(df, 'Anos en Mercado', 'Fecha constitucion')
df= funciones_limpieza.cambio_orden_variable(df, 'Anos desde ultima finanziacion', 'last_funding_date')


# REEMPLAZO DE VALORES AUSENTES
# hay 10 valores que no hay en la columna de sabi, pero si en la de dealroom, por lo que se pasan
df['Numero empleados']= df.loc[:,'Numero empleados'].fillna(df['n_empleados_dealroom'])

# se rellenan los valores de sociedades anonimas con 0 porque la mayoría son sociedades limitadas
df['Sociedad_anonima'] = df['Sociedad_anonima'].fillna(0)

# Primero con formulas financieras

df['Inmovilizado mil EUR']=df['Inmovilizado mil EUR'].fillna(df['Total activo mil EUR'] - df['Activo circulante mil EUR'])
df['Activo circulante mil EUR']=df['Activo circulante mil EUR'].fillna(df['Total activo mil EUR'] - df['Inmovilizado mil EUR'].fillna(0))
df['Total activo mil EUR']=df['Total activo mil EUR'].fillna(df['Total pasivo y capital propio mil EUR'])

df['Pasivo fijo mil EUR']=df['Pasivo fijo mil EUR'].fillna(df['Total pasivo y capital propio mil EUR'].fillna(0)-df['Pasivo liquido mil EUR'].fillna(0)-df['Fondos propios mil EUR'].fillna(0))
df['Pasivo liquido mil EUR']=df['Pasivo liquido mil EUR'].fillna(df['Total pasivo y capital propio mil EUR'].fillna(0)-df['Pasivo fijo mil EUR'].fillna(0)-df['Fondos propios mil EUR'].fillna(0))
df['Total pasivo']=df['Pasivo fijo mil EUR']+df['Pasivo liquido mil EUR']

df['Numero empleados']=df['Numero empleados'].fillna(df['Gastos de personal mil EUR']/(df['Coste medio de los empleados mil']).astype(float, errors='ignore'))
df['Coste medio de los empleados mil']=df['Coste medio de los empleados mil'].fillna(df['Gastos de personal mil EUR']/df['Numero empleados'])
df['Gastos de personal mil EUR']=df['Gastos de personal mil EUR'].fillna(df['Numero empleados']*df['Coste medio de los empleados mil'])
df['Impuestos sobre sociedades mil EUR']=df['Impuestos sobre sociedades mil EUR'].fillna(df['Result. ordinarios antes Impuestos mil EUR']-df['Resultado Actividades Ordinarias mil EUR'])

df.loc[:,'Ratio de liquidez %']=df['Ratio de liquidez %'].fillna(((df['Activo circulante mil EUR'])/(df['Pasivo liquido mil EUR'])))
df.loc[:,'Ratio de solvencia %']=df['Ratio de solvencia %'].fillna(df['Ratio de liquidez %'])
df.loc[:,'Ratio_endeudamiento']=df['Total pasivo y capital propio mil EUR']/df['Total pasivo']

# se define la variable localidad porque se va a utilizar posteriormente para crear un df
localidad= df['Localidad']


# ELIMINACION DE COLUMNAS
# se eliminan las columnas que no se van a utilizar 
lista_columnas= ['name_dealroom', 'Fecha constitucion', 'last_funding_date', 'Localidad', 'Codigo consolidacion', 'Estado',
 'tagline', 'website', 'profile_url', 'n_empleados_dealroom', 'Forma juridica detallada', 'Estado detallado', 'n_missings', 'Forma juridica',
 'company_status',  'first_funding_date', 'Fecha constitucion', 'Resultado Actividades Ordinarias mil EUR', 'revenue_models',
'Inmovilizado material mil EUR', 'Inmovilizado inmaterial mil EUR', 'Existencias mil EUR', 'Rotacion de las existencias %', 
'Inmovilizado material mil EUR', 'Gastos financieros y gastos asimilados mil EUR', 'Free capital mil EUR', 'Otros fondos propios mil EUR'  ]

df= df.drop(lista_columnas, axis=1)


# MAS TRANSFORMACIONES
df.loc[df['Pasivo fijo mil EUR']<0, 'Pasivo fijo mil EUR']=0
df.loc[df['Pasivo liquido mil EUR']<0, 'Pasivo liquido mil EUR']=0

# se crea un df que tiene missings para probarlo con modelos a los que no les importan los missings
df_missings= df.copy()

# se actualiza la lista de variables financieras
variables_financieras_eliminadas= ['Resultado Actividades Ordinarias mil EUR', 'Inmovilizado material mil EUR',
 'Inmovilizado inmaterial mil EUR', 'Existencias mil EUR', 'Rotacion de las existencias %', 
 'Gastos financieros y gastos asimilados mil EUR', 'Tesoreria mil EUR',
  'Otros fondos propios mil EUR']
columnas_financieras_completas= columnas_financieras.drop(['year', 'Codigo_NIF', 'n_missings']).drop(variables_financieras_eliminadas)
columnas_financieras_completas= columnas_financieras_completas.append(pd.Index(['Total pasivo']))

# se ven cuantas columnas tienen 1 o mas missings
print(df.isna().sum()[df.isna().sum()>0].sort_values(ascending=False).count())
variables_con_missings= df.isna().sum()[df.isna().sum()>0].sort_values(ascending=False)
variables_con_missings_columnas= list(variables_con_missings.index)

variables_con_missings_antes_nif= df.isna().sum()[df.isna().sum()>0].sort_values(ascending=False)

# se crea un for para que si una empresa tiene un missing en una columna financiera en un año, se sustituye por el del año anterior o posterior
for nif in df['Codigo_NIF'].unique():
    for columna in variables_con_missings_columnas:
        if df.loc[(df['Codigo_NIF']==nif) & (df['year']==2020), columna].isna().values[0]:
            df.loc[(df['Codigo_NIF']==nif) & (df['year']==2020), columna]=df.loc[(df['Codigo_NIF']==nif) & (df['year']==2021), columna].values[0]
        if df.loc[(df['Codigo_NIF']==nif) & (df['year']==2021), columna].isna().values[0]:
            df.loc[(df['Codigo_NIF']==nif) & (df['year']==2021), columna]=df.loc[(df['Codigo_NIF']==nif) & (df['year']==2020), columna].values[0]

# se eliminan mas variables
variables_eliminar= ['ratio_last_funding','last_round', 'last_funding', 'ownerships', 'Tesoreria mil EUR' ]
df= df.drop(variables_eliminar, axis=1)
df_missings= df_missings.drop(variables_eliminar, axis=1)
 
df.loc[df['growth_stage'].isna(), 'growth_stage']= 0 # se asigna el valor más común
df.loc[df['Deudores mil EUR'].isna(), 'Deudores mil EUR']= 0 # se considera que no hay deudores

# para imputar coste medio de los empleados, se agrupa por CNAE y se calcula el coste medio
df['Codigo primario CNAE adaptado']= df['Codigo primario CNAE 2009'].apply(lambda x: round(x/100,0))

col = ['Coste medio de los empleados mil', 'Costes de los trabajadores / Ingresos de explotacion (%) %', 'Deudas financieras mil EUR', 'Acreedores a L. P. mil EUR',
       'Acreedores comerciales mil EUR', 'Periodo de cobro (dias) dias', 'Margen de beneficio (%) %']

for columna in col:
    df[columna] = df[columna].fillna(df.groupby('Codigo primario CNAE adaptado')[columna].transform('median'))


df= df.drop('Codigo primario CNAE adaptado', axis=1)

# se imputan los ingresos de explotacion
funciones_limpieza.imputacion_reg_lineal(df, 'Ingresos de explotacion mil EUR', 'Deudores mil EUR')

# se imputan los costes de los trabajadores y el numero de empleados
df['Coste medio de los empleados mil']=df['Coste medio de los empleados mil'].fillna(df['Costes de los trabajadores / Ingresos de explotacion (%) %']* df['Ingresos de explotacion mil EUR']/100/df['Numero empleados'])
df['Numero empleados']=df['Numero empleados'].fillna(round((df['Costes de los trabajadores / Ingresos de explotacion (%) %']* df['Ingresos de explotacion mil EUR']/100/df['Coste medio de los empleados mil']),0))
df['Gastos de personal mil EUR']= df['Gastos de personal mil EUR'].fillna(df['Coste medio de los empleados mil']*df['Numero empleados'])

# se crea el margen bruto solamente con los costes de los trabajadores ahora que ya se han imputado
df.loc[:,'Margen_bruto(costes trabajadores)']=(df['Ingresos de explotacion mil EUR']-df['Coste medio de los empleados mil'])/(df['Ingresos de explotacion mil EUR']*100)

# importe neto de ventas con ingresos de explotacion
funciones_limpieza.imputacion_reg_lineal(df, 'Importe neto Cifra de Ventas mil EUR', 'Ingresos de explotacion mil EUR')
# total funding con gastos financieros
funciones_limpieza.imputacion_reg_lineal(df, 'Deudas financieras mil EUR', 'Total pasivo')
funciones_limpieza.imputacion_reg_lineal(df, 'total_funding', 'Gastos financieros mil EUR')
funciones_limpieza.imputacion_reg_lineal(df, 'Acreedores comerciales mil EUR', 'Deudas financieras mil EUR')
funciones_limpieza.imputacion_reg_lineal(df, 'Acreedores a L. P. mil EUR', 'Gastos financieros mil EUR')

# hay 3 valores de importe neto de ventas que son menores que 0, así que se ponen en positivo
df.loc[df['Importe neto Cifra de Ventas mil EUR']<0, 'Importe neto Cifra de Ventas mil EUR']= \
df.loc[df['Importe neto Cifra de Ventas mil EUR']<0, 'Importe neto Cifra de Ventas mil EUR']*-1

# se buscan empresas que no coincida la suma de pasivos y fondos propios con el total de activos
pasivo_empresas=df[round((df['Total pasivo']+ df['Fondos propios mil EUR']),5)!= round(df['Total activo mil EUR'],5)]
df.loc[pasivo_empresas.index, 'Pasivo fijo mil EUR']= (df.loc[pasivo_empresas.index, 'Total activo mil EUR'] - df.loc[pasivo_empresas.index, 'Fondos propios mil EUR']) * 0.47
df.loc[pasivo_empresas.index, 'Pasivo liquido mil EUR']= (df.loc[pasivo_empresas.index, 'Total activo mil EUR'] - df.loc[pasivo_empresas.index, 'Fondos propios mil EUR']) * 0.53

# se corrigen algunas imputaciones 
df.loc[df['Numero empleados']<=0, 'Numero empleados']=1

df=df.applymap(lambda x: 99999 if x== np.inf else x)
df=df.applymap(lambda x: -99999 if x== -np.inf else x)

# creacion de variables
df['Beneficio neto mil EUR']= df['Ingresos de explotacion mil EUR']-df['Gastos de personal mil EUR']
df['ROA']= df['Beneficio neto mil EUR']/df['Total activo mil EUR']
df['Margen_EBITDA']= df['EBITDA mil EUR']/df['Ingresos de explotacion mil EUR']

df_missings = df_missings.drop(['Nombre_sabi'], axis=1)

# se guardan variables para meter a los df de modelos cogiendo 1 de cada 2 filas porque cada empresa tiene 2 filas
startup= df['startup'].iloc[::2]
growth_stage= df['growth_stage'].iloc[::2]
b2b_b2c= df['b2b_b2c'].iloc[::2]
nombre_sabi= df['Nombre_sabi'].iloc[::2]
valoracion= df['valuation_2022'].iloc[::2]
variables = pd.concat([b2b_b2c,nombre_sabi  ], axis=1)
variables_valoracion = pd.concat([startup, growth_stage,b2b_b2c, nombre_sabi, valoracion ], axis=1)
variables_valoracion= variables_valoracion.dropna(subset=['valuation_2022'])

# CREACION DE LOS 2 DFS FINALES PARA LOS MODELOS

df_adquisicion, df_valoracion =funciones_limpieza.creacion_dfs_finales(df, columnas_financieras_completas)
df_adquisicion_missings, df_valoracion_missings =funciones_limpieza.creacion_dfs_finales(df_missings, columnas_financieras_completas)

# DF_GRAFICOS
# otro df especial solo para graficos porque tiene la variable de localidad
df_graficos= df_adquisicion.copy()
df_graficos['Localidad']= localidad

# SELECCION DE VARIABLES PARA LOS MODELOS
df_adquisicion = funciones_limpieza.seleccion_de_variables(df_adquisicion, 'Porcentaje_adquisicion_cat', variables_con_missings_antes_nif)
df_valoracion = funciones_limpieza.seleccion_de_variables(df_valoracion, 'valuation_2022', variables_con_missings_antes_nif)

# se añaden las columnas de nif y nombre
df_adquisicion['Nombre_sabi']= nombre_sabi.values

df_adquisicion = pd.merge(variables, df_adquisicion, on= 'Nombre_sabi', how= 'inner')
df_valoracion = pd.merge(variables_valoracion, df_valoracion, on= 'valuation_2022', how= 'right')

# CREACION DE CSVS
# se crea la carpeta de datos limpios
CARPETA_DATOS_LIMPIOS = 'Datos/Limpios/'
if not os.path.exists(CARPETA_DATOS_LIMPIOS):
    os.makedirs(CARPETA_DATOS_LIMPIOS)


# se guarda el df de adquisicion
df_adquisicion.to_csv(CARPETA_DATOS_LIMPIOS + 'df_adquisicion.csv', index=False)

# se guarda el df de valoracion
df_valoracion.to_csv(CARPETA_DATOS_LIMPIOS + 'df_valoracion.csv', index=False)

# se guarda el df de adquisicion con missings
df_adquisicion_missings.to_csv(CARPETA_DATOS_LIMPIOS + 'df_adquisicion_missings.csv', index=False)

# se guarda el df de valoracion con missings
df_valoracion_missings.to_csv(CARPETA_DATOS_LIMPIOS + 'df_valoracion_missings.csv', index=False)

# se guarda el df de graficos
df_graficos.to_csv(CARPETA_DATOS_LIMPIOS + 'df_graficos.csv', index=False)