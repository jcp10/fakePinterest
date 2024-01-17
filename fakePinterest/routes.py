from flask import render_template, url_for, redirect
from fakePinterest import app, database, bcrypt
from fakePinterest.models import Usuario,Fotos
from flask_login import login_required, login_user, logout_user,current_user
from fakePinterest.forms import formLogin, formCriarConta,formFoto
import os
from werkzeug.utils import secure_filename 

# criar os link das paginas


@app.route('/', methods=['GET', 'POST'])  # aqui sera a minha pagina inicial
def homepage():
    form_login = formLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=form_login)


@app.route('/criarConta', methods=['GET', 'POST'])
def criarConta():
    form_criarconta = formCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(email=form_criarconta.email.data,
                          username=form_criarconta.username.data,
                          senha=senha)

        database.session.add(usuario)
        database.session.commit()

        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('criarConta.html', form=form_criarconta)


@app.route('/perfil/<id_usuario>', methods=["GET","POST"])
@login_required  # o usuario so consegue acessar se estievr logado
def perfil(id_usuario):
    if int(id_usuario) == current_user.id:
        form_foto = formFoto()
        if form_foto.validate_on_submit():
            arquivo=form_foto.foto.data
            nome_seguro= secure_filename(arquivo.filename)
            #salvar o arquivo na pasta fotos_post
            caminho=os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],nome_seguro
            )
            arquivo.save(caminho)


            #registrar o arquivo no banco de dados
            foto=Fotos(imagem=nome_seguro,id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template('perfil.html', usuario=current_user,form=form_foto)
    else:
        usuario=Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/feed')
@login_required
def feed():
    fotos = Fotos.query.order_by(Fotos.data_criacao).all()
    return render_template('feed.html', fotos=fotos)