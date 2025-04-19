import tkinter as tk
from tkinter import ttk, messagebox
from biblioteca import Biblioteca  # importa a lógica existente, salve como biblioteca.py

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.biblioteca = Biblioteca()
        self.criar_interface()

    def criar_interface(self):
        abas = ttk.Notebook(self.root)
        abas.pack(expand=True, fill='both')

        self.aba_livros = ttk.Frame(abas)
        self.aba_emprestimos = ttk.Frame(abas)
        self.aba_resumo = ttk.Frame(abas)

        abas.add(self.aba_livros, text='📚 Livros')
        abas.add(self.aba_emprestimos, text='📕 Empréstimos')
        abas.add(self.aba_resumo, text='📊 Resumo')

        self.criar_aba_livros()
        self.criar_aba_emprestimos()
        self.criar_aba_resumo()

    def criar_aba_livros(self):
        frm = ttk.Frame(self.aba_livros, padding=10)
        frm.pack(fill='x')

        ttk.Label(frm, text="Título:").grid(row=0, column=0, sticky='e')
        self.titulo_entry = ttk.Entry(frm, width=30)
        self.titulo_entry.grid(row=0, column=1)

        ttk.Label(frm, text="Autor:").grid(row=1, column=0, sticky='e')
        self.autor_entry = ttk.Entry(frm, width=30)
        self.autor_entry.grid(row=1, column=1)

        ttk.Label(frm, text="Ano:").grid(row=2, column=0, sticky='e')
        self.ano_entry = ttk.Entry(frm, width=30)
        self.ano_entry.grid(row=2, column=1)

        ttk.Button(frm, text="Adicionar Livro", command=self.adicionar_livro).grid(row=3, column=1, pady=10, sticky='e')

        self.lista_livros = tk.Text(self.aba_livros, height=15, wrap='word')
        self.lista_livros.pack(expand=True, fill='both', padx=10, pady=10)
        self.atualizar_lista_livros()

    def criar_aba_emprestimos(self):
        self.lista_emprestimos = tk.Text(self.aba_emprestimos, height=20, wrap='word')
        self.lista_emprestimos.pack(expand=True, fill='both', padx=10, pady=10)
        self.atualizar_lista_emprestimos()

    def criar_aba_resumo(self):
        self.texto_resumo = tk.Label(self.aba_resumo, font=('Arial', 12), justify='left', padding=20)
        self.texto_resumo.pack()
        self.atualizar_resumo()

    def adicionar_livro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()
        ano = self.ano_entry.get()

        if not titulo or not autor or not ano:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        msg = self.biblioteca.adicionar_livro(titulo, autor, ano)
        messagebox.showinfo("Sucesso", msg)
        self.titulo_entry.delete(0, tk.END)
        self.autor_entry.delete(0, tk.END)
        self.ano_entry.delete(0, tk.END)

        self.atualizar_lista_livros()
        self.atualizar_resumo()

    def atualizar_lista_livros(self):
        self.lista_livros.delete(1.0, tk.END)
        self.lista_livros.insert(tk.END, self.biblioteca.listar_livros())

    def atualizar_lista_emprestimos(self):
        self.lista_emprestimos.delete(1.0, tk.END)
        self.lista_emprestimos.insert(tk.END, self.biblioteca.listar_emprestimos())

    def atualizar_resumo(self):
        self.texto_resumo.config(text=self.biblioteca.resumo_biblioteca())

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.geometry("600x500")
    root.mainloop()
