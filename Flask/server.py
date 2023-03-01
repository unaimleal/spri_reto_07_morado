from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/importarcsv', methods=['GET','POST'])
def importarcsv():
    return render_template('csv.html')

if __name__ == "__main__":
    app.run(debug = True)