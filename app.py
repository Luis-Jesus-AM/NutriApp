from urllib import request
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

usuarios = []


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nutrien")
def nutrien():
    return render_template("nutrien.html")

@app.route("/registros")
def registros():
    return render_template("registros.html")


@app.route("/comida")
def comida():
    return render_template("comida.html")

@app.route("/ingre")
def ingre():
    return render_template("ingre.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    nombre = request.form["nombre"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]

    usuario = {
        "nombre": nombre,
        "email": email,
        "contraseña": contraseña
    }

    usuarios.append(usuario)
    print(usuarios)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
