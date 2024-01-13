from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField
from wtforms.validators import DataRequired, Email, EqualTo,Length,ValidationError
from fakePinterest.models import Usuario

class formLogin(FlaskForm):
    email= StringField('E-mail',validators=[DataRequired(),Email()])
    senha= PasswordField('Senha',validators=[DataRequired()])
    botaoLogar= SubmitField('Fazer login')

    # Verificar se o email está cadastrado.
    def validate_email(self,email):
        usuario=Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Usuário não encontrado.')


class formCriarConta(FlaskForm):
    email= StringField('Email',validators=[DataRequired(),Email()])
    username= StringField('Nome do usuário',validators=[DataRequired()])
    senha=PasswordField('Senha',validators=[DataRequired(),Length(3,20)])
    confirmacaoSenha= PasswordField('Confirmar senha',validators=[DataRequired(),EqualTo('senha')])
    botaoConfirmar=SubmitField('Cadastrar')

    #validando o email ao criar a conta
    def validate_email(self,email):
        usuario=Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email ja cadastrado,faça login para continuar')

class formFoto(FlaskForm):
    foto = FileField('Foto',validators=[DataRequired()])
    botaoConfirmar= SubmitField('Enviar')