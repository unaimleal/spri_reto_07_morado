from flask import Flask,  render_template, request, session
import bbdd.sqlite as sql

app = Flask(__name__)

app.secret_key = 'jshugk'

@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/inicio', methods=['GET','POST'])
def iniciosesion():
    if request.method=='POST':
        usuario=request.form.get('usuario')
        contraseña=request.form.get('contraseña')
        if not sql.nombre_existe(usuario):
            return render_template('registrarse.html')
        if not sql.comprobar_contraseña(usuario,contraseña):
            mensaje=' El usuario o la contraseña no son correctos. Intentelo de nuevo'
            return render_template('inicio.html', mensaje=mensaje)
        return render_template('home.html', usuario=usuario) 
    return render_template('inicio.html')

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


@app.route('/importarcsv', methods=['GET','POST'])
def importarcsv():
    return render_template('csv.html')

@app.route('/selccionmodelo', methods=['GET','POST'])
def seleccionmodelo():
    return render_template('seleccionmodelo.html')

############# Para ver los usuatios y contraseñas #antes de entragar borrar!!!!!!!
@app.route('/consultar')
def consultar():
    registro=sql.consultar_usu()
    return render_template('contraseñayusuario.html', registro=registro)

if __name__ == "__main__":
    app.run(debug = True)