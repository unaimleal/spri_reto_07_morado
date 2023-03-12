from flask import Flask,  render_template, request, session,redirect,url_for
import bbdd.sqlite as sql
import pandas as pd
import pickle as pkl
import os

CARPETA_MODELOS1 = "../modelos/clasificacion"
CARPETA_MODELOS2 = "../modelos/regresion"
modelo_clasificacion = pkl.load(open(os.path.join(CARPETA_MODELOS1,"modelo_lineal.pkl"),"rb"))
modelo_regresion = pkl.load(open(os.path.join(CARPETA_MODELOS2,"modelo_lineal.pkl"),"rb"))



app = Flask(__name__)
columnas_valoracion=['Precio/Venta','Activo circulante mil EUR_2021','Fondos propios mil EUR_2021','Total activo mil EUR_2021','Total pasivo y capital propio mil EUR_2021',
 'Fondo de maniobra mil EUR_2021','Deudores mil EUR_2021','Beneficio neto mil EUR','Ingresos de explotacion mil EUR_2021','Importe neto Cifra de Ventas mil EUR_2021','Pasivo liquido mil EUR_2021','Total pasivo_2021',
 'total_funding','Pasivo fijo mil EUR_2021','Gastos financieros mil EUR_2021','Resultado Explotacion mil EUR_2021','EBIT mil EUR_2021','PER','Resultado del Ejercicio mil EUR_2021','Result. ordinarios antes Impuestos mil EUR_2021','Importe neto Cifra de Ventas mil EUR_ratio']

columnas_adquisicion=['Anos en Mercado','Cash flow mil EUR_2021','EBITDA mil EUR_2021','Inmovilizado mil EUR_2021','Fondos propios mil EUR_2021',
 'Valor agregado mil EUR_2021','Total pasivo_ratio','Inmovilizado mil EUR_ratio','Capital suscrito mil EUR_2021','Capital social mil EUR',
 'Gastos financieros mil EUR_ratio','Gastos de personal mil EUR_2021','Resultado financiero mil EUR_ratio','Total pasivo y capital propio mil EUR_2021','Total activo mil EUR_2021',
 'Gastos financieros mil EUR_2021','Pasivo fijo mil EUR_2021','total_funding']

df_valoracion = pd.read_csv('../Datos/Limpios/df_valoracion.csv')
df_adquisicion = pd.read_csv('../Datos/Limpios/df_adquisicion.csv')

sql.crear_tabla()

app.secret_key = 'jshugk'

@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/inicio', methods=['GET','POST'])
def iniciosesion():
    if request.method=='POST':
        usuario=request.form.get('usuario')
        contraseña=request.form.get('contraseña')
        session['usuario']=usuario
        if not sql.nombre_existe(usuario):
            return render_template('registrarse.html')
        if not sql.comprobar_contraseña(usuario,contraseña):
            mensaje=' El usuario o la contraseña no son correctos. Intentelo de nuevo'
            return render_template('inicio.html', mensaje=mensaje)
        return redirect(url_for("principal")) 
    return render_template ('inicio.html')

@app.route('/paginaprincipal')
def principal():
    return render_template('home.html',usuario=session['usuario'])
   

@app.route('/registro',methods=['GET','POST'])
def registro(): 
    if request.method== 'POST':
        usuario = request.form.get("usuario")
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contraseña = request.form.get("contraseña")
        session['nombre']=nombre
        if sql.nombre_existe(usuario):
            mensaje='Ya hay un usuario con ese nombre. Intentelo con otro'
            return render_template('registro.html', mensaje=mensaje) 
        sql.insert_usuarios(nombre,apellido,correo,usuario,contraseña)
        return render_template('home.html', nombre=nombre)

    return render_template('registrarse.html')

###########################
@app.route('/modelvalidacion', methods=['GET','POST'])
def explvalidacion():
    if request.method=='POST':
        return redirect(url_for('seleccionmetodoval'))
    return render_template('explicacionval.html')

@app.route('/seleccionval', methods=['GET','POST'])
def seleccionmetodoval():
    if request.method=='POST':
        metodo=request.form.get('metodo')
        if metodo=='empresa':
            return redirect(url_for('empresaval'))
        return redirect(url_for('manualval'))
    return render_template('seleccionmetodoval.html')
################################
@app.route('/manualval', methods=['GET','POST'])
def manualval():
    if request.method=='POST':
        df_datos_val=[]
        datos_val={}
        for i in columnas_valoracion:
            datos=request.form.get(i)
            datos_val[i]=datos
        df_datos_val.append(datos_val)
        df_datos_val=pd.DataFrame(df_datos_val)
        print(df_datos_val)
        return 'datos enviados'
    return render_template('manualval.html',columnas=columnas_valoracion)
################################
b2b_b2c = list(df_valoracion['b2b_b2c'].unique())
startup = list(df_valoracion['startup'].unique())

@app.route("/empresaval", methods=['GET','POST'])
def empresaval():
    if request.method=='POST':
        b2=request.form.get('b2')
        start=request.form.get('start')
        select_start=int(start)
        print(b2,type(select_start))
        session['selected_b2'] = b2
        session['selected_start'] = select_start
        filtered_data = df_valoracion[(df_valoracion["b2b_b2c"] == b2) & (df_valoracion["startup"] == select_start) ]['Nombre_sabi']
        linea=[]
        for row in filtered_data.unique():
            linea.append(row)
        print(linea)
        return render_template('resultempresaval.html', row_data=linea,b2b_b2c=b2,startup=start)
    return render_template('empresaval.html', 
                    b2b_b2c = b2b_b2c, 
                    startup = startup)

@app.route('/resultempresaval', methods = ['POST'])
def resultempresaval():
    empresa=request.form.get('row')
    print(empresa)
    return 'modelo'
    
###########################
@app.route('/modeladquisicion', methods=['GET','POST'])
def expladquisicion():
    if request.method=='POST':
         return redirect(url_for('seleccionmetodoad'))
    return render_template('explicacionad.html')

@app.route('/seleccionad', methods=['GET','POST'])
def seleccionmetodoad():
    if request.method=='POST':
        metodo=request.form.get('metodo')
        if metodo=='empresa':
            return render_template('empresad.html')
        return redirect(url_for('manualad'))
    return render_template('seleccionmetodoad.html')

@app.route('/manualad', methods=['GET','POST'])
def manualad():
    if request.method=='POST':
        df_datos_ad=[]
        datos_ad={}
        for i in columnas_adquisicion:
            datos=request.form.get(i)
            datos_ad[i]=datos
        df_datos_ad.append(datos_ad)
        df_datos_ad=pd.DataFrame(df_datos_ad)
        print(df_datos_ad)
        return 'datos enviados'
    return render_template('manualad.html', columnas=columnas_adquisicion)

############################
@app.route('/visualizarmodelos', methods=['GET','POST'])
def selecvisualizar():
    if request.method=='POST':
        visualizamodelo = request.form.get('visualizamodelo')
        if visualizamodelo == 'ad':
            return render_template('resultadosadquisicion.html')
        return render_template('resultadosvalidacion.html')
    return render_template('selecvisualizar.html')



############# Para ver los usuatios y contraseñas #antes de entragar borrar!!!!!!!
@app.route('/consultar')
def consultar():
    registro=sql.consultar_usu()
    return render_template('contraseñayusuario.html', registro=registro)

if __name__ == "__main__":
    app.run(debug = True)