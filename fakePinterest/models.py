from fakePinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader

def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id= database.Column(database.Integer, primary_key= True)
    username= database.Column(database.String, nullable=False)
    email= database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto= database.relationship("Fotos", backref="usuario", lazy=True)

class Fotos(database.Model):  # a modificação está nessa linha
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)