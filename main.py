from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3, os
from werkzeug.utils import secure_filename

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


"""PÁGINA PRODUCTOS"""

@app.route('/productosSeguridad', methods=["GET", "POST"])
def productosSeguridad():
  conn = sqlite3.connect('ginhsonElektronik.db')
  q = f"""SELECT * FROM Productos WHERE linea = 'Seguridad' """
  resu = conn.execute(q)

  productos = []
  imagenProducto = []
  for i in resu:
    productos.append(i)
  for i in productos:
    imagenProducto.append(i[4])
  largo = len(productos)
  conn.commit()      
  conn.close()
  
  return render_template('productosSeguridad.html', productos = productos, largo = largo, imagenProducto = imagenProducto)

@app.route('/productosNautica', methods=["GET", "POST"])
def productosNautica():
  conn = sqlite3.connect('ginhsonElektronik.db')
  q = f"""SELECT * FROM Productos WHERE linea = 'Nautica' """
  resu = conn.execute(q)

  productos = []
  imagenProducto = []
  for i in resu:
    productos.append(i)
  for i in productos:
    imagenProducto.append(i[4])
  largo = len(productos)
  conn.commit()      
  conn.close()
  
  return render_template('productosNautica.html', productos = productos, largo = largo, imagenProducto = imagenProducto)

@app.route('/productosIndustria', methods=["GET", "POST"])
def productosIndustria():
  conn = sqlite3.connect('ginhsonElektronik.db')
  q = f"""SELECT * FROM Productos WHERE linea = 'Industria' """
  resu = conn.execute(q)

  productos = []
  imagenProducto = []
  for i in resu:
    productos.append(i)
  for i in productos:
    imagenProducto.append(i[4])
  largo = len(productos)
  conn.commit()      
  conn.close()
  
  return render_template('productosIndustria.html', productos = productos, largo = largo, imagenProducto = imagenProducto)

@app.route('/productosDispositivos', methods=["GET", "POST"])
def productosDispositivos():
  conn = sqlite3.connect('ginhsonElektronik.db')
  q = f"""SELECT * FROM Productos WHERE linea = 'Dispositivos' """
  resu = conn.execute(q)
  productos = []
  imagenProducto = []
  for i in resu:
    productos.append(i)
  for i in productos:
    imagenProducto.append(i[4])
  largo = len(productos)
  conn.commit()      
  conn.close()
  return render_template('productosDispositivos.html', productos = productos, largo = largo, imagenProducto = imagenProducto)

"""FUNCIONES ADMINISTRADOR"""

@app.route('/admin', methods=["GET", "POST"])
def admin():
  if session['sesion'] == True:
    return redirect('/opcionesAdmin')
  else:
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
  return render_template('opcionesAdmin.html')

@app.route('/agregarProductos', methods=["GET", "POST"])
def agregarProductos():
  if (request.method == "POST"):
    if session['sesion'] == True:
      nombre = request.form["nombre"]
      categoria = request.form["categoria"]
      informacion = request.form["informacion"]
      file = request.files['imagen']
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)
      
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
        mensaje2 = "Por favor renombre el archivo de la imagen, el anterior ya existe en la base de datos."
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
    if session['sesion'] == True:
      if (request.form["nombreProducto"] != ""):
        producto = request.form["nombreProducto"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreProducto = []
        imagenProducto = []
        for i in lista:
          nombreProducto.append(i[0])
        for i in lista:
          imagenProducto.append(i[-1])
        largo = len(nombreProducto)
        conn.commit()      
        conn.close()
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
      producto = request.form["producto"]
      info = request.form["info"]
      if info == "":
        descripcion = False
      else:
        descripcion = True
      conn = sqlite3.connect('ginhsonElektronik.db')     
      q = f"""UPDATE Productos SET informacion = '{info}' and descripcion = '{descripcion}' WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      return jsonify(producto)
    else:
      return redirect('/admin')

@app.route('/modificarCategoria',  methods=["POST", "GET"])
def modificarCategoria():
  if (request.method == "POST"):
    if session['sesion'] == True:
      producto = request.form["producto"]
      categoria = request.form["categoria"]
      print(producto)
      print(categoria)
      conn = sqlite3.connect('ginhsonElektronik.db')     
      q = f"""UPDATE Productos SET categoria = '{categoria}' WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      return jsonify(producto)
    else:
      return redirect('/admin')

@app.route('/modificarLinea',  methods=["POST", "GET"])
def modificarLinea():
  if (request.method == "POST"):
    if session['sesion'] == True:
      producto = request.form["producto"]
      linea = request.form["linea"]
      print(producto)
      print(linea)
      conn = sqlite3.connect('ginhsonElektronik.db')     
      q = f"""UPDATE Productos SET linea = '{linea}' WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      return jsonify(producto)
    else:
      return redirect('/admin')

@app.route('/modificarNombre',  methods=["POST", "GET"])
def modificarNombre():
  if (request.method == "POST"):
    if session['sesion'] == True:
      producto = request.form["producto"]
      nuevoNombre = request.form["nuevoNombre"]
      print(producto)
      print(nuevoNombre)
      conn = sqlite3.connect('ginhsonElektronik.db')     
      q = f"""UPDATE Productos SET nombre = '{nuevoNombre}' WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      return jsonify(producto)
    else:
      return redirect('/admin')

@app.route('/modificarImagen', methods=["POST", "GET", "PUT"])
def modificarImagen():
  if (request.method == "POST"):
    if session['sesion'] == True:
      producto = request.form["producto"]
      print(producto)
      file = request.files["imagen"] # EL ERROR ES ACÁ  
      print("hla")
      print(file)
      if "C:\fakepath" in file:
        file = file.remove('C:\fakepath')
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)
      print(file_path)
      conn = sqlite3.connect('ginhsonElektronik.db')     
      q = f"""UPDATE Productos SET imagen = '{file_path}' WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
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
    producto = request.form["nombreProducto"]
    if session['sesion'] == True:
      if (request.form["nombreProducto"] != "" ):
        producto = request.form["nombreProducto"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreProducto = []
        imagenProducto = []
        for i in lista:
          nombreProducto.append(i[0])
        print(nombreProducto)
        for i in lista:
          imagenProducto.append(i[-1])
        largo = len(nombreProducto)
        print(largo)
        conn.commit()      
        conn.close()
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
      producto = request.form["producto"]
      conn = sqlite3.connect('ginhsonElektronik.db')
      q = f"""DELETE FROM Productos WHERE nombre = '{producto}'"""
      conn.execute(q)
      conn.commit()      
      conn.close()
      return jsonify(producto)
    else:
      return redirect('/admin')


# PRUEBA MODIFICAR IMAGEN EN OTRO HTML

@app.route('/modificaImagen', methods=["GET", "POST"])
def modificaImagen():
  if (request.method == "POST"):
    if session['sesion'] == True:
      nombre = request.form["nombre"]
      file = request.files['imagen']
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)
           
      conn = sqlite3.connect('ginhsonElektronik.db')
      q = f"""SELECT imagen FROM Productos WHERE imagen = '{file_path}'"""
      resu = conn.execute(q)

      if resu.fetchone():
        mensaje2 = "Por favor renombre el archivo de la imagen, el anterior ya existe en la base de datos."
        return render_template('modificarImagen.html', mensaje2 = mensaje2)
      else:  
        r = f"""UPDATE Productos SET imagen = '{file_path}' WHERE nombre = '{nombre}'"""
        conn.execute(r)
        conn.commit()
        conn.close()
      
      return render_template('modificarImagen.html')
    else:
      return redirect('/admin')
  else:
    return render_template('modificarImagen.html')


@app.route('/modificacionImagenBuscador',  methods=["GET", "POST"])
def modificacionImagenBuscador():
  if (request.method == "POST"):
    if session['sesion'] == True:
      if (request.form["nombreProducto"] != ""):
        producto = request.form["nombreProducto"]
        conn = sqlite3.connect('ginhsonElektronik.db')
        r = f"""SELECT nombre, imagen FROM Productos where nombre = '{producto}'"""
        resu = conn.execute(r)
        lista = resu.fetchall()
        nombreProducto = []
        imagenProducto = []
        for i in lista:
          nombreProducto.append(i[0])
        for i in lista:
          imagenProducto.append(i[-1])
        largo = len(nombreProducto)
        conn.commit()      
        conn.close()
        return render_template('modificarImagen.html', productos = nombreProducto, imagenProducto = imagenProducto, largo = largo)
      else:
        mensaje = "Ingrese un nombre"
        return render_template('modificarImagen.html', mensaje = mensaje, largo = largo)
    else:
      return redirect('/admin')  
  else:
    return redirect('/modificaImagen', largo = largo)


app.run(host='0.0.0.0', port=81)