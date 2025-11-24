from flask import Flask, render_template
from flask_wtf import FlaskForm # import FlaskForm from flask_wtf que faz 
from dotenv import load_dotenv #gerencia chaves de ambiente
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import os
from supabase import create_client, Client
# 1. Carrega as variáveis do arquivo .env
load_dotenv()

#conecção com o supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Cria o cliente do Supabase  
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) 

#formulario de cadastro
class CadastroForm(FlaskForm):
    PrimeiroNome = StringField('Primeiro Nome', validators=[DataRequired(), Length(min=2, max=30)])
    Sobrenome = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=30)])
    CPF = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    Email = StringField('Email', validators=[DataRequired(), Email(message='Email inválido')])
    Senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6), EqualTo('ConfirmarSenha', message='As senhas devem ser iguais')])
    ConfirmarSenha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('Senha', message='As senhas devem ser iguais')])
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
    
    if form.validate_on_submit():
        # Coleta os dados do formulário
        primeiro_nome = form.PrimeiroNome.data
        sobrenome = form.Sobrenome.data
        cpf = form.CPF.data
        email = form.Email.data
        senha = form.Senha.data
        
        # Insere os dados no Supabase
        data = {
            'PrimeiroNome': primeiro_nome,
            'SobreNome': sobrenome,
            'CPF': cpf,
            'Email': email,
            'Senha': senha
        }
        try:
            response = supabase.table('Usuários').insert(data).execute()
            
            return 'Cadastro realizado com sucesso!'
        except Exception as e:
            return f'Erro ao conectar com o banco de dados: {e}'
    return render_template('cadastro.html', form=form)
#Fim da rota de cadastro


if __name__ == '__main__':
    app.run(debug=True)
