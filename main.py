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


@app.route('/opcionesAdmin', methods=["GET", "POST"])
def opcionesAdmin():
  return render_template('opcionesAdmin.html')

@app.route('/ingreso', methods=["GET", "POST"])
def ingreso():
  print("llega a ingreso")
  if (request.method == "POST"):
    print("pasa el post")
    if (request.form["usuario"] != "" or request.form["password"] != ""):
      session['sesion'] = True
      session['usuario'] = request.form["usuario"]
      session['contraseña'] = request.form["password"]
      conn = sqlite3.connect('ginhsonElektronik.db')
      q = f"""SELECT * FROM Usuarios WHERE nombre = '{session['usuario']}' and contraseña = '{session['contraseña']}'"""
      resu = conn.execute(q)
      lista = resu.fetchall()
      print(lista)
      if len(lista) != 0:
        if lista[0][0] != session['usuario'] or lista[0][1] != session['contraseña']:
          mensaje = 'Los datos ingresados son incorrectos'
          print('Los datos ingresados son incorrectos')
          return render_template('admin.html', mensaje = mensaje)
      else:
        mensaje = 'Los datos ingresados son incorrectos'
        return render_template('admin.html', mensaje = mensaje)
      conn.commit()      
      conn.close()
      return render_template('opcionesAdmin.html')
    else:
      mensaje = "Por favor rellene todos los campos"
      return render_template('admin.html', mensaje = mensaje)
      
  else:
    return render_template('admin.html')






app.run(host='0.0.0.0', port=81)