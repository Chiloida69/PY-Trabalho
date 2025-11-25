from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Simulação de Banco de Dados (Lista de Dicionários) ---
estoque_mock = [
    {"modelo": "Real Madrid - Torcedor", "ano": 2025, "tamanho": "G", "quantidade": 15},
    {"modelo": "Flamengo - Jogo 1", "ano": 2024, "tamanho": "M", "quantidade": 3},
    {"modelo": "Barcelona - Retro", "ano": 2010, "tamanho": "GG", "quantidade": 8},
    {"modelo": "Brasil - Treino", "ano": 2024, "tamanho": "P", "quantidade": 20},
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/novo_produto')
def novo_produto():
    return render_template('novo_produto.html')

# --- Rota de Consulta ---
@app.route('/consulta', methods=['GET'])
def consulta():
    # Pega o termo digitado na busca (name="q" no HTML)
    termo = request.args.get('q')
    
    lista_exibida = []

    if termo:
        # Se tem pesquisa, filtra a lista
        termo = termo.lower() # transforma em minúsculo pra facilitar
        for produto in estoque_mock:
            if termo in produto['modelo'].lower():
                lista_exibida.append(produto)
    else:
        # Se não tem pesquisa, mostra tudo
        lista_exibida = estoque_mock
        termo = "" # Garante que a variável existe para o template não dar erro

    # Renderiza o template enviando a lista e o termo pesquisado
    return render_template('consulta.html', lista_produtos=lista_exibida, termo_pesquisa=termo)

if __name__ == '__main__':
    app.run(debug=True)