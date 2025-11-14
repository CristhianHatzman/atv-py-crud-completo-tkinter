import tkinter as tk
from tkinter import messagebox, Toplevel, ttk, PhotoImage

from cadastro_pessoas import TelaPessoas
from cadastro_veiculos import TelaVeiculos
from cadastro_lugares import TelaLugares

class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema FATEC - Login")
        self.root.geometry("350x250")
        self.root.configure(bg="#F0F0F0") 

        frame = ttk.Frame(self.root, padding="10")
        frame.pack(expand=True, fill='both')

        frame_form = ttk.Frame(frame)
        frame_form.pack(side='left', padx=10)
        
        ttk.Label(frame_form, text="Usuário:").grid(row=0, column=0, padx=5, pady=10, sticky='w')
        self.entry_usuario = ttk.Entry(frame_form, width=20)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=10)

        ttk.Label(frame_form, text="Senha:").grid(row=1, column=0, padx=5, pady=10, sticky='w')
        self.entry_senha = ttk.Entry(frame_form, show="*", width=20)
        self.entry_senha.grid(row=1, column=1, padx=5, pady=10)

        
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(side='right', padx=10, fill='y')
        
        self.img_entrar = PhotoImage(file="icones/acesso.png")
        self.img_sair = PhotoImage(file="icones/sair.png")

        btn_acessar = ttk.Button(frame_botoes, text="Acessar", image=self.img_entrar, compound=tk.TOP, command=self.fazer_login)
        btn_acessar.pack(pady=5, fill='x')

        btn_sair = ttk.Button(frame_botoes, text="Sair", image=self.img_sair, compound=tk.TOP, command=self.root.destroy)
        btn_sair.pack(pady=5, fill='x')

        self.entry_usuario.focus()
        self.root.bind('<Return>', lambda event: self.fazer_login())

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario == "cristhian" and senha == "12345":
            
            self.root.withdraw() 
            menu_root = Toplevel(self.root)
            TelaMenuPrincipal(menu_root, self.root)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

class TelaMenuPrincipal:
    def __init__(self, root, login_root):
        self.root = root
        self.login_root = login_root
        self.root.title("Menu Principal - Sistema FATEC")
        self.root.geometry("600x600")
        
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_app)

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill='both')

        self.lg_pessoas = PhotoImage(file="icones/logo_usuarios.png")
        self.lg_veiculos = PhotoImage(file="icones/logo_servicos.png")

        ttk.Label(frame, text="Menu Principal - Sistema FATEC", font=("Helvetica", 16)).pack(pady=10)

        btn_pessoas = ttk.Button(frame, text="Controle de Pessoas", image=self.lg_pessoas, compound=tk.LEFT, command=self.abrir_tela_pessoas, padding=10)
        btn_pessoas.pack(pady=10, fill='x')

        btn_veiculos = ttk.Button(frame, text="Controle de Veículos", image=self.lg_veiculos, compound=tk.LEFT, command=self.abrir_tela_veiculos, padding=20)
        btn_veiculos.pack(pady=20, fill='x')

        btn_lugares = ttk.Button(frame, text="Controle de Locais Turísticos", command=self.abrir_tela_lugares, padding=30)
        btn_lugares.pack(pady=30, fill='x')

    def fechar_app(self):
        self.login_root.destroy()

    def abrir_tela_pessoas(self):
        janela_pessoas = Toplevel(self.root)
        TelaPessoas(janela_pessoas)

    def abrir_tela_veiculos(self):
        janela_veiculos = Toplevel(self.root)
        TelaVeiculos(janela_veiculos)

    def abrir_tela_lugares(self):
        janela_lugares = Toplevel(self.root)
        TelaLugares(janela_lugares)


if __name__ == "__main__":
    app_root = tk.Tk()
    style = ttk.Style(app_root)
    
    try:
        style.theme_use('vista') 
    except tk.TclError:
        print("Tema não disponível.")
        
    app = TelaLogin(app_root)
    app_root.mainloop()