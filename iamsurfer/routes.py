# Criando as rotas

from flask import redirect, render_template, url_for
from iamsurfer import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from iamsurfer.forms import FormLogin, FormCriarConta, FormFoto, FormExcluirFoto
from iamsurfer.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename
from flask import abort

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin() 
    if formlogin.validate_on_submit():        
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)

# Criando usuario 
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(username=formcriarconta.username.data, senha=senha,email=formcriarconta.email.data)

        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("criarconta.html", form=formcriarconta)


@app.route("/perfil/<id_usuario>", methods=["GET","POST"])
@login_required  # Função que faz com que só possa ser acessada por algum usuario
def perfil(id_usuario):
# perfil do current_user
    #Formulario de postar foto caso seja o current_user
    if int(id_usuario) == int(current_user.id):
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # Salvar arquivo na pasta
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # salvar o caminho para a pasta no databse
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required

def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()[:20]
    return render_template ("feed.html", fotos=fotos)

@app.route("/excluir_foto/<int:foto_id>", methods=["POST"])
@login_required
def excluir_foto(foto_id):
    foto = Foto.query.get_or_404(foto_id)
    database.session.delete(foto)
    database.session.commit()
    return redirect(url_for('perfil', id_usuario=current_user.id))


    