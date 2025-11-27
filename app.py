from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import requests

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'


mysql = MySQL(app)
app.secret_key = "wey_donde_estoy"

API_KEY = "f6b36cb84f3b46fab7d19b28bcb4c681"
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"



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



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nutrien")
def nutrien():
    return render_template("nutrien.html")


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
@login_requerido
def perfil():
    usuario_id = session.get("id")   

    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre, correo FROM userrs WHERE id = %s", (usuario_id,))
    usuario = cur.fetchone()
    cur.close()

    if usuario is None:
        return "Usuario no encontrado"

    nombre = usuario[0]
    correo = usuario[1]
    inicial = correo[0].upper() 

    return render_template("perfil.html", nombre=nombre, correo=correo, inicial=inicial)


@app.route("/sesion")
def sesion():
    return render_template("sesion.html")

@app.route("/iniciar-sesion", methods=["POST"])
def iniciar_sesion():
    correo = request.form.get("correo")
    password = request.form.get("password")

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM userrs WHERE correo = %s", (correo,))
    usuario = cur.fetchone()
    cur.close()

    if usuario is None:
        return "Usuario no encontrado"


    if usuario[5] == password:
        session["usuario"] = usuario[1]  
        return redirect(url_for("index"))
    else:
        return "Contraseña incorrecta"





@app.route("/registros")
def registros():
    return render_template("registros.html")

@app.route("/gasto", methods=["GET", "POST"])
def gasto():
    resultado_tmb = None
    resultado_get = None
    error = None

    if request.method == "POST":
        try:
            peso = float(request.form["peso"])
            altura = float(request.form["altura"])
            edad = int(request.form["edad"])
            genero = request.form["genero"]
            actividad = request.form["actividad"]

            if peso <= 0 or altura <= 0 or edad <= 0:
                raise ValueError("Todos los valores deben ser positivos.")

            if genero == "hombre":
                tmb = 66.473 + (13.7516 * peso) + (5.0033 * altura) - (6.755 * edad)
            elif genero == "mujer":
                tmb = 655.0955 + (9.5634 * peso) + (1.8496 * altura) - (4.6756 * edad)
            else:
                raise ValueError("Género no válido.")

            factores = {
                "sedentario": 1.2,
                "ligero": 1.375,
                "moderado": 1.55,
                "alto": 1.725,
                "muy_alto": 1.9
            }

            if actividad not in factores:
                raise ValueError("Nivel de actividad no válido.")

            get_total = tmb * factores[actividad]

            resultado_tmb = f"{tmb:.2f}"
            resultado_get = f"{get_total:.2f}"

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("gasto.html",
                           tmb=resultado_tmb,
                           get=resultado_get,
                           error=error)


@app.route("/peso")
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


@app.route("/recetario", methods=["GET", "POST"])
def recetario():
    recipes = None
    ingredient_name = None

    if request.method == "POST":
        ingredient_name = request.form.get("ingredient", "").strip()

        if not ingredient_name:
            flash("Ingresa un ingrediente válido.", "error")
            return redirect(url_for("recetario"))

        try:
            params = {
                "apiKey": API_KEY,
                "query": ingredient_name,  # <-- AQUÍ USAMOS QUERY
                "number": 12,
                "addRecipeInformation": True
            }

            response = requests.get(BASE_URL, params=params)

            if response.status_code != 200:
                flash("Error al conectar con la API.", "error")
                return redirect(url_for("recetario"))

            data = response.json()
            recipes = data.get("results", [])

            return render_template(
                "recetario.html",
                recipes=recipes,
                ingredient_name=ingredient_name
            )

        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for("recetario"))

    return render_template("recetario.html", recipes=None, ingredient_name=None)





@app.route("/macro", methods=["GET", "POST"])
@login_requerido
def macro():
    if request.method == "POST":
        calorias = int(request.form["calorias"])
        objetivo = request.form["objetivo"]

        if objetivo == "perdida":
            p = 0.35
            c = 0.40
            g = 0.25
        elif objetivo == "ganancia":
            p = 0.30
            c = 0.50
            g = 0.20
        else:
            p = 0.30
            c = 0.45
            g = 0.25

        proteina = round((calorias * p) / 4)
        carbohidratos = round((calorias * c) / 4)
        grasas = round((calorias * g) / 9)

        macros = {
            "proteina": proteina,
            "carbohidratos": carbohidratos,
            "grasas": grasas
        }

        return render_template("macro.html", macros=macros)

    return render_template("macro.html")


@app.route("/imc")
def imc():
    return render_template("imc.html")

@app.route("/ejer")
@login_requerido
def ejer():
    return render_template("ejer.html")

@app.route("/imcc", methods=["POST"])
def imcc():
    try:
        peso = float(request.form["peso"])
        altura = float(request.form["altura"]) / 100 

        if altura <= 0 or peso <= 0:
            return render_template("imc.html", error="Valores inválidos")

        imc = round(peso / (altura ** 2), 2)

        
        if imc < 18.5:
            categoria = "Bajo peso"
            mensaje = "Estás flaco 👀"
        elif 18.5 <= imc < 25:
            categoria = "Peso normal"
            mensaje = "Tienes un peso saludable 😄"
        elif 25 <= imc < 30:
            categoria = "Sobrepeso"
            mensaje = "Tienes sobrepeso ⚠️"
        else:
            categoria = "Obesidad"
            mensaje = "Cuidado, estás en obesidad 🚨"

        return render_template("imc.html", imc=imc, categoria=categoria, mensaje=mensaje)

    except:
        return render_template("imc.html", error="Error en los datos ingresados")


@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.pop("usuario", None)
    return redirect(url_for("index"))


@app.route("/registrar", methods=["POST"])
def registrar():
    
    
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    password = request.form.get("password")

    cur = mysql.connection.cursor()


   
    cur.execute("""
        INSERT INTO userrs (nombre, correo, password)
        VALUES (%s, %s, %s)
    """, (nombre, email, password))

    mysql.connection.commit()

    cur.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
