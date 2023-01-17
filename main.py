from flask import Flask, render_template, request, jsonify, session, current_app, redirect
import sqlite3, os
from os.path import abspath, dirname, join
from werkzeug.utils import secure_filename

from email.message import EmailMessage
import smtplib

from flask_mail import Message, Mail  

UPLOAD_FOLDER = './static/media'
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
  return render_template('index.html')


@app.route('/admin')
def admin():
  return render_template('admin.html')


app.run(host='0.0.0.0', port=81)