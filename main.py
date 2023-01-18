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

app.run(host='0.0.0.0', port=81)