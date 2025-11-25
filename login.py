from flask import Flask, render_template
from flask_wtf import FlaskForm # import FlaskForm from flask_wtf que faz 
from dotenv import load_dotenv #gerencia chaves de ambiente
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import os
from supabase import create_client, Client
def login():
    # 1. Carrega as variáveis do arquivo .env
    load_dotenv()

    #conecção com o supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Cria o cliente do Supabase  
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) 

    #formulario de login
    class LoginForm(FlaskForm):
        Email = StringField('Email', validators=[DataRequired(), Email(message='Email inválido')])
        Senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
        Submit = SubmitField('Login')
    #fim do formulario de login

    # Initialize Flask app
    app = Flask(__name__)
    # Ensure SECRET_KEY exists for Flask-WTF CSRF
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'dev-secret-key'

    #Iniciando a rota de login
    @app.route('/templates/login.html', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        
        if form.validate_on_submit():
            # Coleta os dados do formulário
            email = form.Email.data
            senha = form.Senha.data
            
            # Verifica os dados no Supabase
            response = supabase.table('Usuários').select('*').eq('Email', email).eq('Senha', senha).execute()
            usuarios = response.data
            
            if usuarios:
                return render_template('testgratis.html')
            else:
                return "Email ou senha incorretos."
        
        return render_template('login.html', form=form)
    #Fim da rota de login