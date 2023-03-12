# Proyecto de predicción de valoración y adquisición de startups para Spri
Este proyecto está enfocado en hacer predicciones sobre la valoración y adquisición de startups para el grupo Spri. Utilizando técnicas avanzadas de análisis de datos y aprendizaje automático, se ha desarrollado un modelo capaz de predecir la valoración futura de una startup y si es probable que sea adquirida o no.

Este proyecto es esencial para el grupo Spri, ya que les permite tomar decisiones informadas sobre dónde invertir su dinero en el mundo de las startups. Además, también es útil para startups que buscan entender su valor actual y cómo pueden mejorar sus posibilidades de ser adquiridas en el futuro.

El modelo ha sido entrenado y evaluado con un conjunto de datos reales de startups proporcionado por el propio grupo Spri. Se está trabajando en continuar mejorando el modelo y aumentar su precisión, a medida que haya más datos de startups en el futuro.

Este fichero tiene el objetivo de facilitar la comprensión general de todos los archivos que incluye el trabajo realizado en el Reto_07 por el equipo MORADO. Consta de 3 secciones de archivos principales junto con un entorno_MORADO_RETO07 (entorno_MORADO_RETO07.yml). Este proyecto debe de ser ejecutado siguiendo el orden de los archivos y ejecutando cada uno de ellos, es decir, ejecutando en orden cada uno de los archivos presentes.

Para poder recibir una información previa sobre la estructuración del proyecto, a continuación, se explicará brevemente el contenido de cada uno de los distintos archivos y carpetas existentes.


###################### ***OBSERVACIONES PREVIAS*** ######################

·Antes de empezar con la ejecución del proyecto hay que crear un entorno a partir de “entorno_MORADO_RETO07.yml” ejecutando este código:

      conda env create -f entorno_MORADO_RETO07.yml


###################### ***CARPETAS*** ######################

***packages:*** Esta carpeta contiene módulos y funciones que son requeridas y utilizadas para la ejecución de los archivos.

***Flask:*** Contiene todos los scripts/htmls necesarios para ejecutra la aplicación de Flask.

***Graficos:*** Esta carpeta recoge los gráficos realizados en formato .png y .html para hacer un guardado de los distintos tipos de visualizaciones.
 
***modelos:*** Recoge el guardado de los modelos en formato .pkl, está dividido en los modelos de regresión y clasificación.


###################### ***ARCHIVOS*** ######################

***01-preprocesamiento.py:*** Tratamientos de limpieza; valores ausentes, duplicados, outliers, unión de dataframes...etc.

***01-preprocesamiento.ipynb:*** Tratamientos de limpieza; valores ausentes, duplicados, outliers, unión de dataframes...etc.


###########

***02-Analisis descriptivo.ipynb:*** Exploración de los datos desde un aspecto descriptivo, donde se añaden todo tipo de gráficos para comprender los datos.

###########

***03-modelado_adquisicion.ipynb:*** Modelado para la clasificación de la adquisición empresas.

***03-modelado_valoracion.ipynb:*** Modelado para la regresión de la valoración de las empresas.


