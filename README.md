# 📚 Bibliotech

Sistema Web para Gerenciamento de Biblioteca Pública

> Criado com Flask, Bootstrap e Google Books API

---

## ✅ Funcionalidades

- Login e autenticação
- Cadastro de livros
- Empréstimos e devoluções
- Busca por título ou autor
- Importação de livros da Google Books (com capa e sinopse)
- Interface moderna com Bootstrap 5

---

## 🚀 Como executar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/bibliotech.git
cd bibliotech
```

### 2. Crie um ambiente virtual e ative
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação
```bash
python app.py
```

Acesse em: `http://127.0.0.1:8080`

> Login: `admin` | Senha: `1234`

---

## 🌐 Deploy no Render

### Arquivos obrigatórios:
- `requirements.txt`
- `Procfile` (com: `web: gunicorn app:app`)
- `render.yaml` (opcional, para automação)

### Etapas:
1. Crie uma conta em https://render.com
2. Clique em **New > Web Service**
3. Conecte seu GitHub e selecione o repositório
4. Configure:
   - Environment: Python
   - Start Command: `gunicorn app:app`
   - Root Directory: deixe em branco

Após o deploy, o app estará acessível em `https://nomedoseuservico.onrender.com`

---

## 🛠 Tecnologias utilizadas

- [Python 3.9+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/)
- [Google Books API](https://developers.google.com/books/)

---

## 📄 Licença

Projeto desenvolvido para fins educacionais. Livre para uso público.
Ronney Marcos