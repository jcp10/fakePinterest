from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

#criando a aplicação
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URL') 
app.config['SECRET_KEY']='225a184abe15673d7f2a9c6bfc5eb8b6'
app.config['UPLOAD_FOLDER']='static/fotos_posts'


database=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view ='homepage'

from fakePinterest import routes