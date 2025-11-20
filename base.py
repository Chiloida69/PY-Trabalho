from flask import Flask, render_template
from flask_wtf import FlaskForm # import FlaskForm from flask_wtf que faz 
from dotenv import load_dotenv #gerencia chaves de ambiente
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import os
# 1. Carrega as variáveis do arquivo .env
load_dotenv()

#formulario de cadastro
class CadastroForm(FlaskForm):
    PrimeiroNome = StringField('Primeiro Nome', validators=[DataRequired(), Length(min=2, max=30)])
    Sobrenome = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=30)])
    CPF = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    ConfirmarSenha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('Senha', message='As senhas devem coincidir')])
    Submit = SubmitField('Cadastrar')
#fim do formulario de cadastro

# Initialize Flask app
app = Flask(__name__)
# Ensure SECRET_KEY exists for Flask-WTF CSRF
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev-secret-key'
#inicio da rota princiapal/ inicial
@app.route('/')
def main():
    return render_template('testgratis.html')
#Fim da rota principal

#Iniciando a rota de cadastro
@app.route('/templates/cadastro.html', methods=['GET', 'POST'])

def cadastro():
    form = CadastroForm()
    return render_template('cadastro.html', form=form)
#Fim da rota de cadastro


if __name__ == '__main__':
    app.run(debug=True)
