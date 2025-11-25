from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Rota da Home (Exemplo)
@app.route('/')
def home():
    return render_template('home.html')

# Rota de Cadastro de Produto
@app.route('/novo_produto', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        # Aqui o Python captura o que foi digitado nos inputs pelo "name"
        nome_time = request.form['nome_time']
        ano = request.form['ano']
        tamanho = request.form['tamanho']
        quantidade = request.form['quantidade']
        
        # --- AQUI VOCÊ ENTRA COM A LÓGICA DE SALVAR NO BANCO OU LISTA ---
        print(f"Cadastrado: {nome_time} ({ano}) - Tam: {tamanho} - Qtd: {quantidade}")
        
        # Depois de cadastrar, redireciona para a home ou mostra mensagem
        return redirect(url_for('home'))
    
    # Se for GET (apenas acessando a página), mostra o formulário
    return render_template('novo_produto.html')

if __name__ == '__main__':
    app.run(debug=True)