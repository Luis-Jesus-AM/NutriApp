from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

app.secret_key = "wey_donde_estoy"

def calcular_imc(peso, altura_cm):
    altura_m = altura_cm / 100
    imc = peso / (altura_m ** 2)
    return round(imc, 1)

def categoria_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"




def calcular_tmb(peso, altura, edad, genero):
    if genero == 'hombre':
        tmb = 66 + (13.75 * peso) + (5 * altura) - (6.75 * edad)
    elif genero == 'mujer':
        tmb = 655 + (9.56 * peso) + (1.85 * altura) - (4.68 * edad)
    else:
        raise ValueError("Género no válido.")
    return tmb

def calcular_get(tmb, actividad):
    factores_actividad = {
        'sedentario': 1.2,
        'ligero': 1.375,
        'moderado': 1.55,
        'alto': 1.725,
        'muy alto': 1.9
    }
    if actividad not in factores_actividad:
        raise ValueError("Nivel de actividad no válido.")
    return tmb * factores_actividad[actividad]

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
@login_requerido
def nutrien():
    return render_template("nutrien.html")

from flask import request, render_template

@app.route('/calculadora', methods=['GET', 'POST'])
def calculadora_tmb_get():
    contexto = {
        'tmb_resultado': None,
        'get_resultado': None,
        'error': None,
        'peso': None,
        'altura': None,
        'edad': None,
        'genero': None,
        'actividad': None
    }

    if request.method == 'POST':
        try:
            contexto['peso'] = request.form.get('peso')
            contexto['altura'] = request.form.get('altura')
            contexto['edad'] = request.form.get('edad')
            contexto['genero'] = request.form.get('genero')
            contexto['actividad'] = request.form.get('actividad')

            print(f"Peso: {contexto['peso']}, Altura: {contexto['altura']}, Edad: {contexto['edad']}, Género: {contexto['genero']}, Actividad: {contexto['actividad']}")

            if not contexto['peso'] or not contexto['altura'] or not contexto['edad'] or not contexto['genero'] or not contexto['actividad']:
                raise ValueError("Todos los campos deben estar completos.")

            peso_val = float(contexto['peso'])
            altura_val = float(contexto['altura'])
            edad_val = int(contexto['edad'])

            if peso_val <= 0 or altura_val <= 0 or edad_val <= 0:
                raise ValueError("El peso, la altura y la edad deben ser números positivos.")

            print(f"Peso convertido: {peso_val}, Altura convertida: {altura_val}, Edad convertida: {edad_val}")

            tmb_calc = calcular_tmb(peso_val, altura_val, edad_val, contexto['genero'])
            get_calc = calcular_get(tmb_calc, contexto['actividad'])

            print(f"TMB calculado: {tmb_calc}, GET calculado: {get_calc}")

            contexto['tmb_resultado'] = f"{tmb_calc:.2f}"
            contexto['get_resultado'] = f"{get_calc:.2f}"

        except ValueError as e:
            contexto['error'] = f"🚨 {str(e)}"
        except Exception as e:
            contexto['error'] = f"🚨 Ocurrió un error inesperado: {str(e)}"
            print(f"Error inesperado: {e}")

    return render_template('nutrien.html', **contexto)



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


@app.route("/peso")
@login_requerido
def peso():
    return render_template("peso.html")

@app.route("/ideal", methods=["GET", "POST"])
def ideal():
    peso = None
    edad = None
    if request.method == "POST":
        altura = int(request.form["altura"])
        sexo = request.form["sexo"]
        edad = int(request.form["edad"])
        if altura < 152:
            altura = 152
        if sexo == "hombre":
            peso = 50 + 0.9 * (altura - 152)
        else:
            peso = 45.5 + 0.9 * (altura - 152)
        peso = round(peso, 1)
    return render_template("peso.html", peso=peso, edad=edad)


@app.route("/ingre")
@login_requerido
def ingre():
    return render_template("ingre.html")

@app.route("/imc")
@login_requerido
def imc():
    return render_template("imc.html")

@app.route("/imcc", methods=["GET", "POST"])
def imcc():
    imc_val = None
    cat = None
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        imc_val = calcular_imc(peso, altura)
        cat = categoria_imc(imc_val)
    return render_template("imc.html", imcc=imc_val, categoria=cat)

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
