import pymysql
from flask.helpers import url_for
from flask import Flask,render_template,request,redirect,flash
from datetime import datetime


connection=pymysql.connect(
            host="18.222.42.25", # si es remota coloca IP // 192.168.200.50
            user='grupo',
            password='mysql',
            db='robots',)

cursor=connection.cursor()

sql='SELECT * FROM producto_'
try:
    cursor.execute(sql)
    data=cursor.fetchall() # mas de uno
    print(data)
except Exception as e:
    raise

sql='SELECT * FROM cliente_'
try:
    cursor.execute(sql)
    data=cursor.fetchall() # mas de uno
    print(data)
except Exception as e:
    raise

def obtener_productos():
    #alumnosx = []
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM producto_")
            productox = cursor.fetchall()
            return productox
        except Exception as e:
            raise
    #return alumnosx


def obtener_clientes():
    #alumnosx = []
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM cliente_")
            clientex = cursor.fetchall()
            return clientex
        except Exception as e:
            raise
    #return alumnosx

def insertar_cliente(idcliente, direccion, telefono,email,nombres,apellidoP, apellidoM):
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO cliente_(idcliente, direccion, telefono,email,nombres,apellidoP, apellidoM) VALUES (%s, %s, %s, %s, %s, %s, %s)",(idcliente, direccion, telefono,email,nombres,apellidoP, apellidoM))
            connection.commit()
        except Exception as e:
            raise
    
print("Hello World")


app = Flask(__name__)


@app.route('/')
def index():
   #return "Hello World"
   return render_template("index.html")

@app.route("/tienda")
def formulario_agregar_producto():
    producto=obtener_productos()
    return render_template("tienda.html",producto=producto)

# @app.route("/etadisticas")
# def formulario_agregar_alumno():
#     return render_template("estadisticas.html")

# @app.route("/mispedidos")
# def formulario_agregar_alumno():
#     return render_template("mispedidos.html")

# @app.route("/registro")
# def formulario_agregar_alumno():
#     return render_template("registro.html")


# #@app.route("/")
# @app.route("/estadisticas")
# def alumnos():
#     alumno = obtener_alumnos()
#     #return render_template("alumnos.html")
#     return render_template("alumnos.html", alumno=alumno)


# @app.route("/guardar_alumno", methods=["POST"])
# def guardar_alumno():
#     nombre = request.form["nombre"]
#     nota = request.form["nota"]
#     edad = request.form["edad"]
#     insertar_alumno(nombre, nota, edad)
#     # De cualquier modo, y si todo fue bien, redireccionar
#     return redirect("/alumnos")


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
