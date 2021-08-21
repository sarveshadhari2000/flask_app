from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_required,logout_user,current_user,login_user
import re

pan_path = 'documents/PAN/'
aadhar_path = 'documents/AADHAR/'
passbook_path = 'documents/PASSBOOK/'

documents_root = 'documents/'

db = SQLAlchemy()

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/db1'
db.init_app(app)

login_manager = LoginManager() # Create a Login Manager instance
login_manager.login_view = 'login'
login_manager.init_app(app)


