from flask import Flask, render_template, request, jsonify, session, current_app, redirect
import sqlite3, os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename

from email.message import EmailMessage
import smtplib

from flask_mail import Message, Mail  

UPLOAD_FOLDER = './images/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)


app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'info@ginhson.com.ar'
app.config['MAIL_PASSWORD'] = 'imwmdsovtxinssfg'
#huellitas123.
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'esto-es-una-clave-muy-secreta'


@app.route('/')
def index():
  session['sesion'] = False  
  session['Seguridad'] = "."
  session['Industria'] = "."
  session['Nautica'] = "."
  session['Dispositivos'] = "."
  return render_template('index.html')

@app.route('/admin', methods=["GET", "POST"])
def admin():
  if session['sesion'] == True:
    return redirect('/opcionesAdmin')
  else:
    print("def admin con sesion cerrada")
    return render_template('admin.html')


@app.route('/ingreso', methods=["GET", "POST"])
def ingreso():
  if (request.method == "POST"):
    if (request.form["usuario"] != "" or request.form["password"] != ""):
      session['sesion'] = True
      session['usuario'] = request.form["usuario"]
      session['contraseña'] = request.form["password"]
      conn = sqlite3.connect('ginhsonElektronik.db')
      q = f"""SELECT * FROM Usuarios WHERE nombre = '{session['usuario']}' and contraseña = '{session['contraseña']}'"""
      resu = conn.execute(q)
      lista = resu.fetchall()
      if len(lista) != 0:
        if lista[0][1] != session['usuario'] or lista[0][2] != session['contraseña']:
          mensaje = 'Los datos ingresados son incorrectos'
          print('Los datos ingresados son incorrectos')
          return render_template('admin.html', mensaje = mensaje)
      else:
        mensaje = 'Los datos ingresados son incorrectos'
        return render_template('admin.html', mensaje = mensaje)
      conn.commit()      
      conn.close()
      return redirect('/opcionesAdmin')
    else:
      mensaje = "Por favor rellene todos los campos"
      return render_template('admin.html', mensaje = mensaje)
      
  else:
    return render_template('admin.html')


@app.route('/opcionesAdmin', methods=["GET", "POST"])
def opcionesAdmin():
  print("opciones Admin")
  return render_template('opcionesAdmin.html')

@app.route('/agregarProductos', methods=["GET", "POST"])
def agregarProductos():
  print("agregar productos")
  if (request.method == "POST"):
    if session['sesion'] == True:
      nombre = request.form["nombre"]
      nombre = nombre.capitalize()
      categoria = request.form["categoria"]
      informacion = request.form["informacion"]
      file = request.files['imagen']
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      print(file_path)
      file.save(file_path)
      print(request.form.get('linea'))
      
      if request.form.get('linea') == 'Seguridad':
        linea = "Seguridad"
      elif request.form.get('linea') == 'Nautica':
        linea = "Nautica"
      elif request.form.get('linea') == 'Industria':
        linea = "Industria"
      elif request.form.get('linea') == 'Dispositivos':
        linea = "Dispositivos"
      else:
        mensaje = "¡Elija un checkbox!"
        print(mensaje)
        return render_template('agregarProductos.html',
                               mensaje = mensaje)
      
      conn = sqlite3.connect('ginhsonElektronik.db')
      q = f"""SELECT imagen FROM Productos WHERE imagen = '{file_path}'"""
      resu = conn.execute(q)

      if informacion == "":
        descripcion = False
      else:
        descripcion = True
      
      if resu.fetchone():
        mensaje2 = "Por favor renombre el archivo, el anterior ya existe."
        return render_template('agregarProductos.html', mensaje2 = mensaje2)
      else:  
        r = f"""INSERT INTO Productos (nombre, linea, descripcion, imagen, informacion, categoria) VALUES ('{nombre}', '{linea}', '{descripcion}', '{file_path}', '{informacion}', '{categoria}');"""
        conn.execute(r)
        conn.commit()
        conn.close()
      
      return render_template('agregarProductos.html')
    else:
      return redirect('/admin')
  else:
    return render_template('agregarProductos.html')

@app.route('/borrarProductos', methods=["GET", "POST"])
def borrarProductos():
  if session['sesion'] == True:
    largoS = 0
    largoI = 0
    largoN = 0
    largoD = 0
    return render_template('borrarProductos.html', largoS = largoS, largoI = largoI, largoN = largoN, largoD = largoD)
  else:
    return redirect('/admin')

@app.route('/modificarProductos', methods=["GET", "POST"])
def modificarProductos():
  print("modificar productos")
  return render_template('modificarProductos.html')

@app.route('/borrarProductosGeneral', methods=["GET", "POST"])
def borrarProductosGeneral():
  if session['sesion'] == True:
    largo = 0
    return render_template('borrarProductosGeneral.html', largo = largo)
  else:
    return redirect('/admin')

@app.route('/opcionesBorrarProducto',  methods=["GET", "POST"])
def opcionesBorrarProducto():
  if (request.method == "POST"):
    print('hola')
    producto = request.form["nombreProducto"]
    print(producto)
    if session['sesion'] == True:
      if (request.form["nombreProducto"] != "" ):
        producto = request.form["nombreProducto"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        producto = producto.capitalize()
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        print(producto)
        resu = conn.execute(r)
        print(resu)
        lista = resu.fetchall()
        nombreProducto = []
        imagenProducto = []
        for i in lista:
          nombreProducto.append(i[0])
        print(nombreProducto)
        for i in lista:
          imagenProducto.append(i[-1])
        print(imagenProducto)
        largo = len(nombreProducto)
        conn.commit()      
        conn.close()
        
        return render_template('borrarProductosGeneral.html', productos = nombreProducto, imagenProducto = nombreProducto, largo = largo)
      else:
        mensaje = "Ingrese un nombre"
        return render_template('borrarProductosGeneral.html', mensaje = mensaje, largo = largo)
    else:
      return redirect('/admin')  
  else:
    return redirect('/borrarProductosGeneral', largo = largo)

@app.route('/opcionesBorrarProductoSeguridad',  methods=["GET", "POST"])
def opcionesBorrarProductoSeguridad():
  if (request.method == "POST"):
    if session['sesion'] == True:
      if (request.form["nombreProductoSeguridad"] != "" and session['Nautica'] == "." and session['Industria'] == "." and session['Dispositivos'] == "."):
        producto = request.form["nombreProductoSeguridad"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        producto = producto.capitalize()
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        print(producto)
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreProductoSeguridad = []
        imagenProductoSeguridad = []
        for i in lista:
          nombreProductoSeguridad.append(i[0])
        print(nombreProductoSeguridad)
        for i in lista:
          imagenProductoSeguridad.append(i[-1])
        print(imagenProductoSeguridad)
        largoS = len(nombreProductoSeguridad)
        largoI = 0
        largoN = 0
        largoD = 0
        conn.commit()      
        conn.close()
        
        return render_template('borrarProductos.html', nombreProductoSeguridad = nombreProductoSeguridad, imagenProductoSeguridad = nombreProductoSeguridad, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
  
      else:
        largoS = 0
        largoI = 0
        largoN = 0
        largoD = 0
        mensajeS = "Ingrese un nombre"
        return render_template('borrarProductos.html', mensajeS = mensajeS, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
    else:
      return redirect('/admin')  
  else:
    largoS = 0
    largoI = 0
    largoN = 0
    largoD = 0
    return redirect('/borrarProductos', largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)

@app.route('/opcionesBorrarProductoNautica',  methods=["GET", "POST"])
def opcionesBorrarProductoNautica():
  if (request.method == "POST"):
    if session['sesion'] == True:
      if (request.form["nombreProductoNautica"] != "" and session['Seguridad'] == "." and session['Industria'] == "." and session['Dispositivos'] == "."):
        producto = request.form["nombreProductoNautica"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        producto = producto.capitalize()
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        print(producto)
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreProductoNautica = []
        imagenProductoNautica = []
        for i in lista:
          nombreProductoNautica.append(i[0])
        print(nombreProductoNautica)
        for i in lista:
          imagenProductoNautica.append(i[-1])
        print(imagenProductoNautica)
        largoN = len(nombreProductoNautica)
        largoI = 0
        largoS = 0
        largoD = 0
        conn.commit()      
        conn.close()
        
        return render_template('borrarProductos.html', nombreProductoNautica = nombreProductoNautica, imagenProductoNautica = nombreProductoNautica, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
  
      else:
        largoS = 0
        largoI = 0
        largoN = 0
        largoD = 0
        mensajeN = "Ingrese un nombre"
        return render_template('borrarProductos.html', mensajeN = mensajeN, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
    else:
      return redirect('/admin')  
  else:
    largoS = 0
    largoI = 0
    largoN = 0
    largoD = 0
    return redirect('/borrarProductos', largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)

@app.route('/opcionesBorrarProductoIndustria',  methods=["GET", "POST"])
def opcionesBorrarProductoIndustria():
  if (request.method == "POST"):
    if session['sesion'] == True:
      if (request.form["nombreProductoIndustria"] != "" and session['Nautica'] == "." and session['Seguridad'] == "." and session['Dispositivos'] == "."):
        producto = request.form["nombreProductoIndustria"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        producto = producto.capitalize()
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        print(producto)
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreProductoIndustria = []
        imagenProductoIndustria = []
        for i in lista:
          nombreProductoIndustria.append(i[0])
        print(nombreProductoIndustria)
        for i in lista:
          imagenProductoIndustria.append(i[-1])
        print(imagenProductoIndustria)
        largoI = len(nombreProductoIndustria)
        largoS = 0
        largoN = 0
        largoD = 0
        conn.commit()      
        conn.close()
        
        return render_template('borrarProductos.html', nombreProductoIndustria = nombreProductoIndustria, imagenProductoIndustria = nombreProductoIndustria, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
  
      else:
        largoS = 0
        largoI = 0
        largoN = 0
        largoD = 0
        mensajeI = "Ingrese un nombre"
        return render_template('borrarProductos.html', mensajeI = mensajeI, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
    else:
      return redirect('/admin')  
  else:
    largoS = 0
    largoI = 0
    largoN = 0
    largoD = 0
    return redirect('/borrarProductos', largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)

@app.route('/opcionesBorrarProductoDispositivos',  methods=["GET", "POST"])
def opcionesBorrarProductoDispositivos():
  if (request.method == "POST"):
    if session['sesion'] == True:
      if (request.form["nombreProductoDispositivos"] != "" and session['Seguridad'] == "." and session['Industria'] == "." and session['Nautica'] == "."):
        producto = request.form["nombreProductoDispositivos"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        producto = producto.capitalize()
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        print(producto)
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreProductoDispositivos = []
        imagenProductoDispositivos = []
        for i in lista:
          nombreProductoDispositivos.append(i[0])
        print(nombreProductoDispositivos)
        for i in lista:
          imagenProductoDispositivos.append(i[-1])
        print(imagenProductoDispositivos)
        largoD = len(nombreProductoDispositivos)
        largoI = 0
        largoS = 0
        largoN = 0
        conn.commit()      
        conn.close()
        
        return render_template('borrarProductos.html', productosDispositivos = nombreProductoDispositivos, imagenProductoDispositivos = nombreProductoDispositivos, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
  
      else:
        largoS = 0
        largoI = 0
        largoN = 0
        largoD = 0
        mensajeD = "Ingrese un nombre"
        return render_template('borrarProductos.html', mensajeD = mensajeD, largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)
    else:
      return redirect('/admin')  
  else:
    largoS = 0
    largoI = 0
    largoN = 0
    largoD = 0
    return redirect('/borrarProductos', largoI = largoI, largoS = largoS, largoN = largoN, largoD = largoD)



@app.route('/eliminar', methods=["POST"])
def eliminar():
  if (request.method == "POST"):
    if session['sesion'] == True:
      print("hla")
      nombre = request.form["nombre"]
      producto = request.form["producto"]
      print(producto)
      conn = sqlite3.connect('ginhsonElektronik.db')
      if producto == "Seguridad":
        print("Seguridad")
        q = f"""DELETE FROM Productos WHERE nombre = '{nombre}'"""
      elif producto == "Nautica":
        print("Nautica")
        q = f"""DELETE FROM Productos WHERE nombre = '{nombre}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      print(nombre)
      return jsonify(nombre)
    else:
      return redirect('/formularioRefugio')


app.run(host='0.0.0.0', port=81)