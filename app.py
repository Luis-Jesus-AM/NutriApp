from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

app.secret_key = "clave_super_secreta"

def login_requerido(ruta):
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("sesion"))
        return ruta(*args, **kwargs)
    wrapper.__name__ = ruta.__name__
    return wrapper

usuarios = [
    {
        "nombre": "luis",
        "email": "23308060610060@cetis61.edu.mx",
        "contraseña": "123456"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nutrien")
def nutrien():
    return render_template("nutrien.html")


@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/sesion")
def sesion():
    return render_template("sesion.html")

@app.route("/iniciar-sesion", methods=["POST"])
def iniciar_sesion():
    email = request.form["email"]
    contraseña = request.form["contraseña"]

    for u in usuarios:
        if u["email"] == email and u["contraseña"] == contraseña:
            session["usuario"] = email   
            return redirect(url_for("index"))

    return "Usuario o contraseña incorrectos"



@app.route("/registros")
def registros():
    return render_template("registros.html")

@app.route("/comida")
@login_requerido
def comida():
    return render_template("comida.html")

@app.route("/ingre")
@login_requerido
def ingre():
    return render_template("ingre.html")

@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("usuario", None)
    return redirect(url_for("index"))


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

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
