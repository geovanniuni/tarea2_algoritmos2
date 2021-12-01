import pymysql
from flask.helpers import url_for
from flask import Flask,render_template,request,redirect,flash
from datetime import datetime

#Clases
class carritoCompra:
    fechaCreacion=None
    listaLineaProducto=None
  
    def __init__(self,fcx,lx=[]):
        self.__fechaCreacion=fcx
        self.listaLineaProducto=lx   
    def getFecha(self):
        return self.fechaCreacion
    def getListaLineas(self):
        return self.listaLineaProducto
    def addLineaProducto(self,newLine):
        self.listaLineaProducto.append(newLine)
    def getTotalCarrito(self):
        total=0
        for i in range(len(self.listaLineaProducto)):
            total+=self.listaLineaProducto[i].getPrecioLinea()
        return total
    def printCarrito(self):
        for i in range(len(self.listaLineaProducto)):
            self.listaLineaProducto[i].printLinea()
      
    

class lineaProducto:
    cantidad=None
    precioLinea=None
    productox=None
    def __init__(self,cantx,prox):
        self.cantidad=cantx
        self.productox=prox
        self.precioLinea=prox.getPrecioProducto()*cantx
        
    def getCantidad(self):
        return self.cantidad
    def getPrecioLinea(self):
        return self.precioLinea
    def getProductox(self):
        return self.productox
    
    def printLinea(self):
        print(self.productox.procedencia+" "+str(self.cantidad), end=' ')
        print("$"+ str(self.productox.getPrecioProducto()), end=' ')
        print("$"+str(self.precioLinea))

class producto:
    idProducto=None
    precioProducto=None
    stock=None
    proveedor=None
    procedencia=None
    def __init__(self,idx,preciox,stockx,provx,procx):
        self.idProducto=idx
        self.precioProducto=preciox
        self.stock=stockx
        self.proveedor= provx
        self.procedencia=procx
       
    def getIdProducto(self):
        return self.idProducto
    def getProcedencia(self):
        return self.procedencia
    def getProveedor(self):
        return self.proveedor
    def getPrecioProducto(self):
        return self.precioProducto
    def getStock(self):
        return self.stock
        
class pedido:
    idPedido=None
    fechaRealizacion=None
    estado=None
    total=None
    carritox=None
    def __init__(self,idx,frx,fcx,lx=[]):
        self.idPedido=idx
        self.fechaRealizacion=frx
        self.estado="Proceso"
        self.carritox=carritoCompra(fcx,lx)
    def getIdPedido(self):
        return self.idPedido
    def getFechaRealizacion(self):
        return self.fechaRealizacion
    def getEstado(self):
        return self.estado
    def getCarritox(self):
        return self.carritox
    def finalizarPedido(self):
        self.estado="Finalizado"
    def printPedido(self):
        print(self.idPedido,end=" ")
        print(self.estado,end=" ")
        print(self.fechaRealizacion)
        self.carritox.printCarrito()
        print("Total Pedido $"+str(self.carritox.getTotalCarrito()))
        print("\n")
    
        
class cliente:
    idCliente=None
    nombre=None
    correo=None
    contraseña=None
    listaPedidos=None
    def __init__(self,idx,nomx,corrx,contrax):
        self.idCliente=idx
        self.nombre=nomx
        self.correo=corrx
        self.contraseña=contrax
        self.listaPedidos=[]
        
    def getIdCliente(self):
        return self.idCliente
    def getNombre(self):
        return self.nombre
    def getCorreo(self):
        return self.correo
    def getContraseña(self):
        return self.contraseña
    def getPedidos(self):
        return self.listaPedidos
    def setPedidox(self,pedido):
        self.listaPedidos.append(pedido)
    def finalizarPedidox(self,idPedidox):
        for i in range(len(self.listaPedidos)):
            if(idPedidox==self.listaPedidos[i].getIdPedido()):
                self.listaPedidos[i].finalizarPedido()
    def testPedidos(self):
        for i in range(len(self.listaPedidos)):
            self.listaPedidos[i].printPedido()
            
    



#Conectar
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
def lista_productos():
    productox= obtener_productos()
    listaDeProductos=[]
    for i in productox:
        prod=producto(i[0],i[1],i[2],i[3],i[4])
        listaDeProductos.append(prod)
    return listaDeProductos




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

def lista_clientes():
    clientex= obtener_clientes()
    listaDeClientes=[]
    for i in clientex:
        cli=cliente(i[0],i[1],i[2], i[3])
        listaDeClientes.append(cli)
    return listaDeClientes

def insertar_cliente(idcliente, nombre, correo,contraseña):
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO cliente_(idcliente, nombre, correo,contraseña) VALUES (%s, %s, %s, %s)",(idcliente, nombre, correo,contraseña))
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


@app.route("/guardar_lineaPedido", methods=["POST"])
def guardar_lineaPedido(clientex,productox):
    cantidad = request.form["cantidad"] #Recibe cantidad del producto
    idpedido = request.form["idpedido"]
    nuevaLinea= lineaProducto(cantidad,productox)
    existe=False
    for i in clientex.getPedidos():
        if(i.getIdPedido==idpedido):
            existe=True
            i.getCarritox().addLineaProducto(nuevaLinea)
    if not existe:
        nuevoPedido= pedido(idpedido,"No disponible","No disponible")
        nuevoPedido.getCarritox().addLineaProducto(nuevaLinea)
        clientex.setPedidos(nuevoPedido)

    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/tienda")

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
