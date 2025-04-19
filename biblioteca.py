import json
import uuid
import os

class Biblioteca:
    def __init__(self, caminho_arquivo='biblioteca.json'):
        self.caminho_arquivo = caminho_arquivo
        self.livros = []
        self.emprestimos = []
        self.carregar_dados()

    def salvar_dados(self):
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump({'livros': self.livros, 'emprestimos': self.emprestimos}, f, indent=4)

    def carregar_dados(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.livros = dados.get('livros', [])
                self.emprestimos = dados.get('emprestimos', [])

    def adicionar_livro(self, titulo, autor, ano):
        titulo = titulo.strip()
        livro = {
            'id': str(uuid.uuid4()),
            'titulo': titulo,
            'autor': autor.strip(),
            'ano': ano.strip(),
            'disponivel': True
        }
        self.livros.append(livro)
        self.salvar_dados()
        return f"Livro '{titulo}' adicionado com sucesso. ID: {livro['id']}."

    def remover_livro(self, id_livro):
        for livro in self.livros:
            if livro['id'] == id_livro and livro['disponivel']:
                self.livros.remove(livro)
                self.salvar_dados()
                return f"Livro '{livro['titulo']}' removido com sucesso."
        return "Livro não encontrado ou está emprestado."

    def listar_livros(self):
        if not self.livros:
            return "Nenhum livro cadastrado na biblioteca."
        lista = "Livros cadastrados:\n"
        for livro in self.livros:
            status = "Disponível" if livro['disponivel'] else "Emprestado"
            lista += f"- [{livro['id'][:8]}] {livro['titulo']} (Autor: {livro['autor']}, Ano: {livro['ano']}) - {status}\n"
        return lista

    def emprestar_livro(self, id_livro, aluno):
        for livro in self.livros:
            if livro['id'] == id_livro and livro['disponivel']:
                livro['disponivel'] = False
                self.emprestimos.append({'id': id_livro, 'titulo': livro['titulo'], 'aluno': aluno.strip()})
                self.salvar_dados()
                return f"Livro '{livro['titulo']}' emprestado para {aluno}."
        return "Livro não encontrado ou indisponível."

    def devolver_livro(self, id_livro, aluno):
        for emprestimo in self.emprestimos:
            if emprestimo['id'] == id_livro and emprestimo['aluno'].lower() == aluno.strip().lower():
                for livro in self.livros:
                    if livro['id'] == id_livro:
                        livro['disponivel'] = True
                        self.emprestimos.remove(emprestimo)
                        self.salvar_dados()
                        return f"Livro '{livro['titulo']}' devolvido por {aluno}."
        return "Empréstimo não encontrado."

    def listar_emprestimos(self):
        if not self.emprestimos:
            return "Nenhum empréstimo registrado."
        lista = "Empréstimos atuais:\n"
        for emp in self.emprestimos:
            lista += f"- [{emp['id'][:8]}] {emp['titulo']} emprestado para {emp['aluno']}\n"
        return lista

    def resumo_biblioteca(self):
        total = len(self.livros)
        emprestados = len(self.emprestimos)
        disponiveis = total - emprestados
        return f"📚 Total de livros: {total} | 📗 Disponíveis: {disponiveis} | 📕 Emprestados: {emprestados}"


def menu():
    biblioteca = Biblioteca()
    while True:
        print("\n--- Sistema de Biblioteca ---")
        print("1. Adicionar livro")
        print("2. Remover livro")
        print("3. Listar livros")
        print("4. Emprestar livro")
        print("5. Devolver livro")
        print("6. Listar empréstimos")
        print("7. Resumo da biblioteca")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            ano = input("Ano: ")
            print(biblioteca.adicionar_livro(titulo, autor, ano))
        elif opcao == "2":
            id_livro = input("ID do livro a remover: ")
            print(biblioteca.remover_livro(id_livro.strip()))
        elif opcao == "3":
            print(biblioteca.listar_livros())
        elif opcao == "4":
            id_livro = input("ID do livro a emprestar: ")
            aluno = input("Nome do aluno: ")
            print(biblioteca.emprestar_livro(id_livro.strip(), aluno))
        elif opcao == "5":
            id_livro = input("ID do livro a devolver: ")
            aluno = input("Nome do aluno: ")
            print(biblioteca.devolver_livro(id_livro.strip(), aluno))
        elif opcao == "6":
            print(biblioteca.listar_emprestimos())
        elif opcao == "7":
            print(biblioteca.resumo_biblioteca())
        elif opcao == "0":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
