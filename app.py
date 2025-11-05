from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nutrien")
def nutrien():
    return render_template("nutrien.html")

@app.route("/comida")
def comida():
    return render_template("comida.html")

@app.route("/ingre")
def ingre():
    return render_template("ingre.html")

@app.route("/iniciar")
def iniciar():
    return render_template("iniciar.html")

if __name__ == "__main__":
    app.run(debug=True)
