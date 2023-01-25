from flask import Flask, render_template, request, jsonify, session, current_app, redirect
import sqlite3, os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename

from email.message import EmailMessage
import smtplib

from flask_mail import Message, Mail  

UPLOAD_FOLDER = './static/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)


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
  if session['sesion'] == True:
    largo = 0
    return render_template('modificarProductos.html', largo = largo)
  else:
    return redirect('/admin')

@app.route('/opcionesModificar',  methods=["GET", "POST"])
def opcionesModificar():
  if (request.method == "POST"):
    print('hola')
    '''
    producto = request.form["nombreProducto"]
    print(producto)
    '''
    if session['sesion'] == True:
      if (request.form["nombreProducto"] != ""):
        producto = request.form["nombreProducto"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        producto = producto.capitalize()
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        print(producto)
        resu = conn.execute(r)
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
        print(imagenProducto)
        return render_template('modificarProductos.html', productos = nombreProducto, imagenProducto = imagenProducto, largo = largo)
      else:
        mensaje = "Ingrese un nombre"
        return render_template('modificarProductos.html', mensaje = mensaje, largo = largo)
    else:
      return redirect('/admin')  
  else:
    return redirect('/modificarProductos', largo = largo)

@app.route('/modificar',  methods=["POST", "GET"])
def modificar():
  if (request.method == "POST"):
    if session['sesion'] == True:
      print("hla")
      producto = request.form["producto"]
      info = request.form["info"]
      print("hla2")
      print(producto)
      print(info)
      conn = sqlite3.connect('ginhsonElektronik.db')     
      q = f"""UPDATE Productos SET informacion = '{info}' WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      print(producto)
      return jsonify(producto)
    else:
      return redirect('/admin')

@app.route('/modificarImagen', methods=["POST", "GET", "PUT"])
def modificarImagen():
  if (request.method == "POST"):
    if session['sesion'] == True:
      print("hla")
      producto = request.form["producto"]
      print("hla2")
      print(producto)
      file = request.files["imagen"]
     # old_file = file.replace("C:\fakepath", "")
    #new_file = os.path.join(app.config['UPLOAD_FOLDER'], file)
      #file = os.rename(old_file, new_file)


      
      print("hla3")
      print(file)
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)
      print(file_path)
      conn = sqlite3.connect('ginhsonElektronik.db')     
      q = f"""UPDATE Productos SET imagen = '{file_path}' WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      print(producto)
      return jsonify(producto)
    else:
      return redirect('/admin')

  
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
        print(imagenProducto)
        return render_template('borrarProductosGeneral.html', productos = nombreProducto, imagenProducto = imagenProducto, largo = largo)
      else:
        mensaje = "Ingrese un nombre"
        return render_template('borrarProductosGeneral.html', mensaje = mensaje, largo = largo)
    else:
      return redirect('/admin')  
  else:
    return redirect('/borrarProductosGeneral', largo = largo)



@app.route('/eliminar', methods=["GET", "POST"])
def eliminar():
  if (request.method == "POST"):
    if session['sesion'] == True:
      print("hla")
      producto = request.form["producto"]
      print("hla2")
      print(producto)
      conn = sqlite3.connect('ginhsonElektronik.db')
      print("hla3")
      q = f"""DELETE FROM Productos WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      print(producto)
      return jsonify(producto)
    else:
      return redirect('/admin')


app.run(host='0.0.0.0', port=81)

"""Pagina Productos"""

@app.route('/productosSeguridad')
def productosSeguridad():
  return render_template('productosSeguridad.html')