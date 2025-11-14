import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, filedialog, PhotoImage
from database import conectar_db
from PIL import Image, ImageTk
from datetime import datetime
from bson.objectid import ObjectId

class TelaPessoas:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Pessoas")
        self.root.geometry("700x650")
        self.root.configure(bg="#F0F0F0") 

        self.db = conectar_db()
        if self.db is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao MongoDB.")
            self.root.destroy()
            return
        self.collection = self.db['pessoas']
        
        self.documento_id_carregado = None
        self.caminho_imagem = tk.StringVar()

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        frame_esquerda = ttk.Frame(self.root, padding=8)
        frame_esquerda.grid(row=0, column=0, sticky='nw')

        frame_direita = ttk.Frame(self.root, padding=8)
        frame_direita.grid(row=0, column=1, sticky='nsew')

        frame_botoes = ttk.Frame(self.root, padding=6)
        frame_botoes.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(6,2))
        frame_botoes.columnconfigure(0, weight=1)
        frame_botoes.columnconfigure(1, weight=0)

        frame_resumo = ttk.Frame(self.root, padding=10)
        frame_resumo.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.label_imagem = tk.Label(frame_esquerda, text="[Sem Imagem]", relief="solid", width=12, height=7, anchor='center')
        self.label_imagem.pack(padx=4, pady=4)

        btn_escolher_img = ttk.Button(frame_esquerda, text="Escolher imagem", command=self.escolher_imagem)
        btn_escolher_img.pack(padx=4, pady=(2,4))

        ttk.Label(frame_direita, text="Código:").grid(row=0, column=0, padx=6, pady=4, sticky='w')
        self.entry_codigo = ttk.Entry(frame_direita, width=6)
        self.entry_codigo.grid(row=0, column=1, padx=6, pady=4, sticky='w')

        ttk.Label(frame_direita, text="Idade:").grid(row=0, column=2, padx=6, pady=4, sticky='e')
        self.entry_idade = ttk.Entry(frame_direita, width=6)
        self.entry_idade.grid(row=0, column=3, padx=6, pady=4, sticky='w')

        ttk.Label(frame_direita, text="Nome:").grid(row=1, column=0, padx=6, pady=4, sticky='w')
        self.entry_nome = ttk.Entry(frame_direita, width=48)
        self.entry_nome.grid(row=1, column=1, columnspan=3, padx=6, pady=4, sticky='w')

        self.var_sexo = tk.StringVar(value="M")
        ttk.Label(frame_direita, text="Sexo:").grid(row=2, column=0, padx=6, pady=4, sticky='w')
        rb_frame = ttk.Frame(frame_direita)
        rb_frame.grid(row=2, column=1, sticky='w')
        ttk.Radiobutton(rb_frame, text="M", variable=self.var_sexo, value="M").pack(side='left')
        ttk.Radiobutton(rb_frame, text="F", variable=self.var_sexo, value="F").pack(side='left', padx=6)

        ttk.Label(frame_direita, text="Altura:").grid(row=2, column=2, padx=6, pady=4, sticky='e')
        self.entry_altura = ttk.Entry(frame_direita, width=10)
        self.entry_altura.grid(row=2, column=3, padx=6, pady=4, sticky='w')

        ttk.Label(frame_direita, text="Peso:").grid(row=3, column=0, padx=6, pady=4, sticky='w')
        self.entry_peso = ttk.Entry(frame_direita, width=10)
        self.entry_peso.grid(row=3, column=1, padx=6, pady=4, sticky='w')

        ttk.Label(frame_direita, text="Cidade:").grid(row=3, column=2, padx=6, pady=4, sticky='e')
        self.combo_cidade = ttk.Combobox(frame_direita, values=["Registro", "São Paulo", "Curitiba", "Outra"], width=18)
        self.combo_cidade.grid(row=3, column=3, padx=6, pady=4, sticky='w')
        self.combo_cidade.set("Registro")

        ttk.Label(frame_direita, text="Data Nasc:").grid(row=4, column=0, padx=6, pady=4, sticky='w')
        self.entry_data_nasc = ttk.Entry(frame_direita, width=20)
        self.entry_data_nasc.grid(row=4, column=1, padx=6, pady=4, sticky='w')

        ttk.Label(frame_direita, text="Data Cadastro:").grid(row=4, column=2, padx=6, pady=4, sticky='e')
        self.entry_data_cadastro = ttk.Entry(frame_direita, state='readonly', width=20)
        self.entry_data_cadastro.grid(row=4, column=3, padx=6, pady=4, sticky='w')

        ttk.Label(frame_direita, text="Data Atualização:").grid(row=5, column=0, padx=6, pady=4, sticky='w')
        self.entry_data_atualizacao = ttk.Entry(frame_direita, state='readonly', width=20)
        self.entry_data_atualizacao.grid(row=5, column=1, padx=6, pady=4, sticky='w')

        ttk.Label(frame_direita, text="Descrição:").grid(row=6, column=0, padx=6, pady=4, sticky='w')
        self.entry_descricao = ttk.Entry(frame_direita, width=48)
        self.entry_descricao.grid(row=6, column=1, columnspan=3, padx=6, pady=4, sticky='w')

        self.img_cadastrar = PhotoImage(file="icones/salvar.png")
        self.img_alterar = PhotoImage(file="icones/alterar.png")
        self.img_excluir = PhotoImage(file="icones/excluir.png")

        btn_frame_center = ttk.Frame(frame_botoes)
        btn_frame_center.grid(row=0, column=0)
        btn_salvar = ttk.Button(btn_frame_center, text="Salvar", image=self.img_cadastrar, compound='left', command=self.salvar)
        btn_salvar.pack(side='left', padx=8)
        btn_excluir = ttk.Button(btn_frame_center, text="Excluir", image=self.img_excluir, compound='left', command=self.excluir)
        btn_excluir.pack(side='left', padx=8)
        btn_alterar = ttk.Button(btn_frame_center, text="Alterar", image=self.img_alterar, compound='left', command=self.alterar)
        btn_alterar.pack(side='left', padx=8)
        btn_consultar = ttk.Button(btn_frame_center, text="Consultar", command=self.consultar)
        btn_consultar.pack(side='left', padx=8)
        btn_limpar = ttk.Button(btn_frame_center, text="Limpar", command=self.limpar_campos)
        btn_limpar.pack(side='left', padx=8)

        btn_frame_right = ttk.Frame(frame_botoes)
        btn_frame_right.grid(row=0, column=1, sticky='e', padx=8)
        btn_sair = ttk.Button(btn_frame_right, text="Sair", command=self.root.destroy)
        btn_sair.pack()

        self.label_resumo = ttk.Label(frame_resumo, text="Resumo...", relief="groove", anchor='w')
        self.label_resumo.pack(fill='x', padx=6, pady=(0,6))

        cols = ("codigo", "nome", "idade", "sexo", "cidade")
        self.tree = ttk.Treeview(frame_resumo, columns=cols, show='headings', height=6)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=120)

        vsb = ttk.Scrollbar(frame_resumo, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True, padx=(6,0), pady=4)
        vsb.pack(side='left', fill='y', pady=4)

        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.on_tree_double_click)

        self.carregar_lista()

    def carregar_imagem(self, caminho):
        try:
            img = Image.open(caminho)
            img.thumbnail((150, 150)) 
            self.photo = ImageTk.PhotoImage(img)
            self.label_imagem.config(image=self.photo, text="")
            self.caminho_imagem.set(caminho)
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.label_imagem.config(image=None, text="[Imagem Inválida]")

    def escolher_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if caminho:
            self.carregar_imagem(caminho)

    def coletar_dados_form(self):
        
        return {
            "codigo": self.entry_codigo.get(),
            "nome": self.entry_nome.get(),
            "sexo": self.var_sexo.get(),
            "altura": self.entry_altura.get(),
            "peso": self.entry_peso.get(),
            "idade": self.entry_idade.get(),
            "cidade": self.combo_cidade.get(),
            "data_nasc": self.entry_data_nasc.get(),
            "descricao": self.entry_descricao.get(),
            "caminho_imagem": self.caminho_imagem.get(),
        }

    def popular_form(self, data):
        
        self.entry_codigo.delete(0, 'end'); self.entry_codigo.insert(0, data.get("codigo", ""))
        self.entry_nome.delete(0, 'end'); self.entry_nome.insert(0, data.get("nome", ""))
        self.var_sexo.set(data.get("sexo", "M"))
        self.entry_altura.delete(0, 'end'); self.entry_altura.insert(0, data.get("altura", ""))
        self.entry_peso.delete(0, 'end'); self.entry_peso.insert(0, data.get("peso", ""))
        self.entry_idade.delete(0, 'end'); self.entry_idade.insert(0, data.get("idade", ""))
        self.combo_cidade.set(data.get("cidade", ""))
        self.entry_data_nasc.delete(0, 'end'); self.entry_data_nasc.insert(0, data.get("data_nasc", ""))
        self.entry_descricao.delete(0, 'end'); self.entry_descricao.insert(0, data.get("descricao", ""))
        
        
        self.entry_data_cadastro.config(state='normal')
        self.entry_data_cadastro.delete(0, 'end'); self.entry_data_cadastro.insert(0, data.get("data_cadastro", ""))
        self.entry_data_cadastro.config(state='readonly')
        
        self.entry_data_atualizacao.config(state='normal')
        self.entry_data_atualizacao.delete(0, 'end'); self.entry_data_atualizacao.insert(0, data.get("data_atualizacao", ""))
        self.entry_data_atualizacao.config(state='readonly')
        
        
        caminho_img = data.get("caminho_imagem", "")
        if caminho_img:
            self.carregar_imagem(caminho_img)
        else:
            self.label_imagem.config(image=None, text="[Sem Imagem]")
        
        
        self.documento_id_carregado = data.get("_id")
        self.atualizar_resumo(data)

    def limpar_campos(self):
        self.popular_form({})
        self.documento_id_carregado = None
        # reset imagem
        self.label_imagem.config(image=None, text="[Sem Imagem]")
        self.caminho_imagem.set("")
        self.entry_codigo.focus()

    def carregar_lista(self):
        """Carrega todos os registros da coleção para a Treeview."""
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)

            for doc in self.collection.find().sort("codigo", 1):
                codigo = doc.get("codigo", "")
                nome = doc.get("nome", "")
                idade = doc.get("idade", "")
                sexo = doc.get("sexo", "")
                cidade = doc.get("cidade", "")
                iid = str(doc.get("_id"))
                self.tree.insert('', 'end', iid=iid, values=(codigo, nome, idade, sexo, cidade))
        except Exception as e:
            print(f"Erro ao carregar lista: {e}")

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        try:
            doc = self.collection.find_one({"_id": ObjectId(iid)})
            if doc:
                self.popular_form(doc)
        except Exception:
            vals = self.tree.item(iid, 'values')
            if vals:
                codigo = vals[0]
                doc = self.collection.find_one({"codigo": codigo})
                if doc:
                    self.popular_form(doc)

    def on_tree_double_click(self, event):
        self.on_tree_select(event)

    def atualizar_resumo(self, data):
        
        resumo = f"Código: {data.get('codigo', '')}  Nome: {data.get('nome', '')}  Idade: {data.get('idade', '')}  Sexo: {data.get('sexo', '')}  Cidade: {data.get('cidade', '')}"
        self.label_resumo.config(text=resumo)

    def salvar(self):
        """ Salva um NOVO registro. """
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atenção", "O campo 'Código' é obrigatório para salvar.")
            return

        
        if self.collection.find_one({"codigo": codigo}):
            messagebox.showerror("Erro", "Já existe um registro com este Código. Use 'Alterar'.")
            return
            
        data = self.coletar_dados_form()
        data["codigo"] = codigo
        data["data_cadastro"] = datetime.now().strftime("%d-%m-%Y %H:%M")
        data["data_atualizacao"] = "" 
        
        try:
            result = self.collection.insert_one(data)
            self.documento_id_carregado = result.inserted_id

            self.entry_data_cadastro.config(state='normal')
            self.entry_data_cadastro.delete(0, 'end'); self.entry_data_cadastro.insert(0, data.get("data_cadastro", ""))
            self.entry_data_cadastro.config(state='readonly')

            self.entry_data_atualizacao.config(state='normal')
            self.entry_data_atualizacao.delete(0, 'end'); self.entry_data_atualizacao.insert(0, "")
            self.entry_data_atualizacao.config(state='readonly')

            self.atualizar_resumo(data)
            messagebox.showinfo("Sucesso", "Pessoa salva com sucesso!")
            try:
                self.carregar_lista()
                self.tree.selection_set(str(self.documento_id_carregado))
                self.tree.see(str(self.documento_id_carregado))
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def alterar(self):
        
        if not self.documento_id_carregado:
            messagebox.showwarning("Atenção", "Consulte um registro antes de tentar alterar.")
            return
            
        data = self.coletar_dados_form()
        data["data_atualizacao"] = datetime.now().strftime("%d-%m-%Y %H:%M")
        
        try:
            self.collection.update_one(
                {"_id": self.documento_id_carregado},
                {"$set": data}
            )
            messagebox.showinfo("Sucesso", "Registro alterado com sucesso!")
            self.atualizar_resumo(data)
            try:
                self.carregar_lista()
                if self.documento_id_carregado:
                    self.tree.selection_set(str(self.documento_id_carregado))
                    self.tree.see(str(self.documento_id_carregado))
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar: {e}")

    def consultar(self):
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atenção", "Digite o 'Código' para consultar.")
            return

        try:
            data = self.collection.find_one({"codigo": codigo})
            if data:
                self.popular_form(data)
                try:
                    self.tree.selection_set(str(data.get("_id")))
                    self.tree.see(str(data.get("_id")))
                except Exception:
                    pass
            else:
                messagebox.showinfo("Não encontrado", "Nenhum registro encontrado com este Código.")
                self.limpar_campos()
                self.entry_codigo.insert(0, codigo) 
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar: {e}")

    def excluir(self):
        
        if not self.documento_id_carregado:
            messagebox.showwarning("Atenção", "Consulte um registro antes de tentar excluir.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este registro?"):
            try:
                self.collection.delete_one({"_id": self.documento_id_carregado})
                messagebox.showinfo("Sucesso", "Registro excluído.")
                try:
                    self.carregar_lista()
                except Exception:
                    pass
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")