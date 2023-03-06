from flask import Flask,  render_template, request, session


app = Flask(__name__)

app.secret_key = 'jshugk'

@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/form', methods = ['POST', 'GET']) 
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos'] 
        session['nombre'] = nombre
        session['apellidos'] = apellidos
        if (len(session['nombre']) == 0) & (len(session['apellidos']) == 0):
            mens = 'Por favor, introduzca su nombre y apellidos.'
            return render_template("form.html", mens = mens)    
        
        genero = request.form['genero']
        if genero == 'Mujer':
            ending = 'a'
        elif genero == 'Hombre':
            ending = 'o'
        else:
            ending = 'x'
        mens = f'Bienvenid{ending}, {nombre} {apellidos}.'

        return render_template("home.html", 
                             mens = mens)
    else:
        return render_template("form.html")

@app.route('/importarcsv', methods=['GET','POST'])
def importarcsv():
    return render_template('csv.html')

@app.route('/selccionmodelo', methods=['GET','POST'])
def seleccionmodelo():
    return render_template('seleccionmodelo.html')

if __name__ == "__main__":
    app.run(debug = True)