from flask import Flask, render_template, request, redirect, url_for
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


#formulario de login
class Login_F(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Email(message='Email inválido')])
    Senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    Submit = SubmitField('Login')
#fim do formulario de login

    

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
            
            return render_template('login.html')
        except Exception as e:
            return f'Erro ao conectar com o banco de dados: {e}'
    return render_template('cadastro.html', form=form)
#Fim da rota de cadastro


#Iniciando a rota de login
@app.route('/templates/login.html', methods=['GET','POST'])
def login():
    form = Login_F()
    
    if form.validate_on_submit():
        email = form.Email.data
        senha = form.Senha.data
        
        try:
            # Consulta no Supabase
            response = supabase.table('Usuários').select('*').eq('Email', email).eq('Senha', senha).execute()
            usuarios = response.data # Isso é uma lista: [] se vazio, ou [{...}] se achou
            
            # Verificação correta: se a lista 'usuarios' tiver algo dentro, o login é válido
            if usuarios: 
                return render_template('home.html')
            else:
                return "Falha no login. Email ou senha incorretos."
                
        except Exception as e:
            return f"Erro de conexão: {e}"
    
    # Se o formulário não for válido (ou se for apenas carregar a página), mostra os erros se houver
    if form.errors:
        print("Erros de validação:", form.errors)

    return render_template('login.html', form=form)
#Fim da rota de login    
@app.route('/templates/home.html')
def home():
    return render_template('home.html') 


# Rota de Cadastro de Produto
@app.route('/novo_produto', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        # 1. Captura o que foi digitado nos inputs pelo "name"
        nome_time = request.form['nome_time']
        ano = request.form['ano']
        tamanho = request.form['tamanho']
        quantidade = request.form['quantidade']
        modelo = request.form['modelo']  # Adicionando o campo 'modelo' conforme esperado na consulta
        
        # 2. Cria o dicionário para enviar ao Supabase
        # IMPORTANTE: As chaves (Lado esquerdo) devem ser EXATAMENTE iguais 
        # aos nomes das colunas criadas no seu banco de dados Supabase.
        data_produto = {
            'NomeTime': nome_time,    # Verifique se a coluna no banco é 'NomeTime' ou 'nome_time'
            'Ano': int(ano),          # Convertendo para número inteiro
            'Tamanho': tamanho,
            'Quantidade': int(quantidade), # Convertendo para número inteiro
            'Modelo': modelo  # Adicionando o campo 'modelo' conforme esperado na consulta
        }

        try:
            # 3. Insere na tabela 'Produtos'
            response = supabase.table('Produtos').insert(data_produto).execute()
            
            # Depois de cadastrar com sucesso, redireciona para a home
            return redirect(url_for('home'))
            
        except Exception as e:
            return f"Erro ao cadastrar o produto no banco: {e}"
    
    # Se for GET (apenas acessando a página), mostra o formulário
    return render_template('novo_produto.html')


# --- Rota de Consulta ---
@app.route('/consulta', methods=['GET'])
def consulta():
    # Pega o termo digitado na busca (name="q" no HTML)
    termo = request.args.get('q')
    
    lista_exibida = []

    try:
        if termo:
            # Se tem pesquisa, busca no Supabase filtrando pela coluna 'NomeTime'
            # ilike faz uma busca que ignora maiúsculas/minúsculas (case-insensitive)
            # O f'%{termo}%' serve para buscar o texto em qualquer parte do nome
            response = supabase.table('Produtos').select('*').ilike('NomeTime', f'%{termo}%').execute()
        else:
            # Se não tem pesquisa, busca TODOS os produtos
            response = supabase.table('Produtos').select('*').execute()
        
        # O Supabase retorna os dados dentro de response.data
        lista_exibida = response.data

    except Exception as e:
        print(f"Erro ao buscar dados no Supabase: {e}")
        lista_exibida = []

    # Renderiza o template enviando a lista e o termo pesquisado
    # Importante: termo if termo else "" evita enviar None para o HTML
    return render_template('estoque.html', lista_produtos=lista_exibida, termo_pesquisa=termo if termo else "")
    

if __name__ == '__main__':
    app.run(debug=True)
