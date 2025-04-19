from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import requests
from biblioteca import Biblioteca

app = Flask(__name__)
app.secret_key = 'bibliotech_segredo123'

bib = Biblioteca()

# Decorador para proteger rotas

def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha == '1234':
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            erro = 'Usuário ou senha inválidos.'
    return render_template('login.html', erro=erro)

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/')
@login_obrigatorio
def index():
    return render_template('index.html')

@app.route('/livros')
@login_obrigatorio
def listar_livros():
    livros = bib.livros
    return render_template('livros.html', livros=livros)

@app.route('/adicionar', methods=['GET', 'POST'])
@login_obrigatorio
def adicionar_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        bib.adicionar_livro(titulo, autor, ano)
        return redirect(url_for('listar_livros'))
    return render_template('adicionar.html')

@app.route('/emprestar', methods=['GET', 'POST'])
@login_obrigatorio
def emprestar_livro():
    if request.method == 'POST':
        id_livro = request.form['id']
        aluno = request.form['aluno']
        bib.emprestar_livro(id_livro, aluno)
        return redirect(url_for('listar_emprestimos'))
    livros_disponiveis = [l for l in bib.livros if l['disponivel']]
    return render_template('emprestar.html', livros=livros_disponiveis)

@app.route('/devolver', methods=['GET', 'POST'])
@login_obrigatorio
def devolver_livro():
    if request.method == 'POST':
        id_livro = request.form['id']
        aluno = request.form['aluno']
        bib.devolver_livro(id_livro, aluno)
        return redirect(url_for('listar_emprestimos'))
    return render_template('devolver.html', emprestimos=bib.emprestimos)

@app.route('/listar_emprestimos')
@login_obrigatorio
def listar_emprestimos():
    emprestimos = bib.emprestimos
    return render_template('emprestimos.html', emprestimos=emprestimos)

@app.route('/buscar', methods=['GET', 'POST'])
@login_obrigatorio
def buscar_livros():
    resultados = []
    termo = ''
    if request.method == 'POST':
        termo = request.form['termo'].strip().lower()
        resultados = [
            livro for livro in bib.livros
            if termo in livro['titulo'].lower() or termo in livro['autor'].lower()
        ]
    return render_template('buscar.html', resultados=resultados, termo=termo)

@app.route('/buscar_google', methods=['GET', 'POST'])
@login_obrigatorio
def buscar_google():
    livros_encontrados = []
    termo = ''
    if request.method == 'POST':
        termo = request.form['termo'].strip()
        url = f"https://www.googleapis.com/books/v1/volumes?q={termo}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                livros_encontrados.append({
                    'titulo': volume_info.get('title', 'Sem título'),
                    'autor': ', '.join(volume_info.get('authors', ['Desconhecido'])),
                    'ano': volume_info.get('publishedDate', '')[:4] or '----',
                    'descricao': volume_info.get('description', 'Sem descrição disponível.'),
                    'capa': volume_info.get('imageLinks', {}).get('thumbnail', '')
                })
    return render_template('buscar_google.html', resultados=livros_encontrados, termo=termo)

@app.route('/importar_livro', methods=['POST'])
@login_obrigatorio
def importar_livro():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano = request.form['ano']
    bib.adicionar_livro(titulo, autor, ano)
    return redirect(url_for('listar_livros'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
