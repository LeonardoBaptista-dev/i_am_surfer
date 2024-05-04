# criando os forms
# lembrar de instalar o email_validator
# estrutura da classe
from flask_wtf import FlaskForm 
# campos de texto do meu form
from wtforms import FileField, StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from iamsurfer.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators =[DataRequired(),Email()] )
    senha = PasswordField ("Senha", validators =[DataRequired(),Length(6, 20)] )
    botao = SubmitField ("Fazer Login")
    

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators =[DataRequired(),Email()] )
    username = StringField("Nome de Usuário", validators =[DataRequired()] )
    senha = PasswordField ("Senha", validators =[DataRequired(),Length(6, 20)] )
    confirmacao_senha = PasswordField ("Confirme sua senha", validators =[DataRequired(),EqualTo("senha")])
    botao_confirmacao = SubmitField ("Criar Conta")  

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario: 
            return ValidationError("Email ja cadastrado, faça login para continuar")
    
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario: 
            return ValidationError("Nome de usuário já cadastrado, escolha outro nome para continuar")
        

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_enviar = SubmitField("Enviar")
    
        
class FormExcluirFoto(FlaskForm):
    botao_excluir = SubmitField("Excluir")

