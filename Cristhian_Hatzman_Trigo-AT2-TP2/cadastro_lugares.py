import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, filedialog, PhotoImage
from database import conectar_db
from bson.objectid import ObjectId
from PIL import Image, ImageTk

class TelaLugares:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Locais Turísticos")
        self.root.geometry("900x600")
        self.root.configure(bg="#F0F0F0")

        self.db = conectar_db()
        if self.db is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao MongoDB.")
            self.root.destroy()
            return
        self.collection = self.db['lugares_turisticos']
        
        self.documento_id_carregado = None
        self.caminho_imagem = tk.StringVar()

        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill='x', padx=10, pady=(10, 0))

        frame_form = ttk.Labelframe(top_frame, text='Dados do Local', padding=10)
        frame_form.grid(row=0, column=0, sticky='nsew')

        frame_img = ttk.Labelframe(top_frame, text='Imagem', padding=10)
        frame_img.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        top_frame.columnconfigure(0, weight=3)
        top_frame.columnconfigure(1, weight=2)

        frame_botoes = ttk.Frame(self.root, padding=8)
        frame_botoes.pack(pady=10)

        ttk.Label(frame_form, text="Código:").grid(row=0, column=0, padx=6, pady=6, sticky='w')
        self.entry_codigo = ttk.Entry(frame_form, width=12)
        self.entry_codigo.grid(row=0, column=1, padx=6, pady=6, sticky='w')

        ttk.Label(frame_form, text="Nome Local:").grid(row=1, column=0, padx=6, pady=6, sticky='w')
        self.entry_nome_local = ttk.Entry(frame_form, width=36)
        self.entry_nome_local.grid(row=1, column=1, columnspan=2, padx=6, pady=6, sticky='w')

        ttk.Label(frame_form, text="Cidade:").grid(row=2, column=0, padx=6, pady=6, sticky='w')
        self.entry_cidade = ttk.Entry(frame_form, width=24)
        self.entry_cidade.grid(row=2, column=1, padx=6, pady=6, sticky='w')

        ttk.Label(frame_form, text="Valor Entrada:").grid(row=3, column=0, padx=6, pady=6, sticky='w')
        self.entry_valor = ttk.Entry(frame_form, width=18)
        self.entry_valor.grid(row=3, column=1, padx=6, pady=6, sticky='w')

        ttk.Label(frame_form, text="Estado:").grid(row=4, column=0, padx=6, pady=6, sticky='w')
        estados = ["SP", "MG", "RJ", "PR", "SC", "RS", "Outro"]
        self.combo_estado = ttk.Combobox(frame_form, values=estados, width=16)
        self.combo_estado.grid(row=4, column=1, padx=6, pady=6, sticky='w')

        self.var_guia = tk.StringVar(value="Não")
        ttk.Label(frame_form, text="Necessita Guia:").grid(row=5, column=0, padx=6, pady=6, sticky='w')
        frame_radio_guia = ttk.Frame(frame_form)
        frame_radio_guia.grid(row=5, column=1, sticky='w')
        ttk.Radiobutton(frame_radio_guia, text="Sim", variable=self.var_guia, value="Sim").pack(side='left')
        ttk.Radiobutton(frame_radio_guia, text="Não", variable=self.var_guia, value="Não").pack(side='left', padx=8)

        self.label_imagem = tk.Label(frame_img, text="[Sem Imagem]", relief="solid", width=28, height=12, anchor='center')
        self.label_imagem.pack(padx=6, pady=(0,8))

        btn_escolher_img = ttk.Button(frame_img, text="Escolher Imagem", command=self.escolher_imagem)
        btn_escolher_img.pack()

        self.img_cadastrar = PhotoImage(file="icones/salvar.png")
        self.img_alterar = PhotoImage(file="icones/alterar.png")
        self.img_excluir = PhotoImage(file="icones/excluir.png")

        btn_salvar = ttk.Button(frame_botoes, text="Salvar", image=self.img_cadastrar, compound='left', command=self.salvar)
        btn_salvar.grid(row=0, column=0, padx=6)
        btn_alterar = ttk.Button(frame_botoes, text="Alterar", image=self.img_alterar, compound='left', command=self.alterar)
        btn_alterar.grid(row=0, column=1, padx=6)
        btn_consultar = ttk.Button(frame_botoes, text="Consultar", command=self.consultar)
        btn_consultar.grid(row=0, column=2, padx=6)
        btn_excluir = ttk.Button(frame_botoes, text="Excluir", image=self.img_excluir, compound='left', command=self.excluir)
        btn_excluir.grid(row=0, column=3, padx=6)
        btn_limpar = ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos)
        btn_limpar.grid(row=0, column=4, padx=6)
        btn_sair = ttk.Button(frame_botoes, text="Sair", command=self.root.destroy)
        btn_sair.grid(row=0, column=5, padx=6)

        frame_listagem = ttk.Frame(self.root, padding=10)
        frame_listagem.pack(padx=10, pady=(0,10), fill='both', expand=True)

        cols = ("codigo", "nome_local", "cidade", "estado")
        self.tree = ttk.Treeview(frame_listagem, columns=cols, show='headings', height=6)
        for c in cols:
            self.tree.heading(c, text=c.replace('_', ' ').capitalize())
            self.tree.column(c, width=180 if c == 'nome_local' else 120)

        vsb = ttk.Scrollbar(frame_listagem, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True, padx=(0,5))
        vsb.pack(side='left', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.on_tree_double_click)

        self.carregar_lista()
        
    def escolher_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if caminho:
            self.carregar_imagem(caminho)

    def carregar_imagem(self, caminho):
        try:
            img = Image.open(caminho)
            img.thumbnail((150, 150))
            self.photo = ImageTk.PhotoImage(img)
            self.label_imagem.config(image=self.photo, text="")
            self.caminho_imagem.set(caminho)
        except Exception as e:
            self.label_imagem.config(image=None, text="[Imagem Inválida]")

    def coletar_dados_form(self):
        return {
            "codigo": self.entry_codigo.get(),
            "nome_local": self.entry_nome_local.get(),
            "cidade": self.entry_cidade.get(),
            "valor_entrada": self.entry_valor.get(),
            "estado": self.combo_estado.get(),
            "necessita_guia": self.var_guia.get(),
            "caminho_imagem": self.caminho_imagem.get(),
        }

    def popular_form(self, data):
        self.entry_codigo.delete(0, 'end'); self.entry_codigo.insert(0, data.get("codigo", ""))
        self.entry_nome_local.delete(0, 'end'); self.entry_nome_local.insert(0, data.get("nome_local", ""))
        self.entry_cidade.delete(0, 'end'); self.entry_cidade.insert(0, data.get("cidade", ""))
        self.entry_valor.delete(0, 'end'); self.entry_valor.insert(0, data.get("valor_entrada", ""))
        self.combo_estado.set(data.get("estado", ""))
        self.var_guia.set(data.get("necessita_guia", "Não"))
        
        caminho_img = data.get("caminho_imagem", "")
        if caminho_img:
            self.carregar_imagem(caminho_img)
        else:
            self.label_imagem.config(image=None, text="[Sem Imagem]")
        
        self.documento_id_carregado = data.get("_id")

    def limpar_campos(self):
        self.popular_form({})
        self.documento_id_carregado = None
        self.entry_codigo.focus()

    def carregar_lista(self):
        """Carrega todos os registros da coleção para a Treeview."""
        try:
            for i in self.tree.get_children():
                self.tree.delete(i)

            for doc in self.collection.find().sort("codigo", 1):
                codigo = doc.get("codigo", "")
                nome = doc.get("nome_local", "")
                cidade = doc.get("cidade", "")
                estado = doc.get("estado", "")
                iid = str(doc.get("_id"))
                self.tree.insert('', 'end', iid=iid, values=(codigo, nome, cidade, estado))
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
                nome = vals[1]
                doc = self.collection.find_one({"nome_local": nome})
                if doc:
                    self.popular_form(doc)

    def on_tree_double_click(self, event):
        self.on_tree_select(event)

    def salvar(self):
        nome = self.entry_nome_local.get()
        if not nome:
            messagebox.showwarning("Atenção", "O 'Nome Local' é obrigatório para salvar.")
            return

        if self.collection.find_one({"nome_local": nome}):
            messagebox.showerror("Erro", "Já existe um local com este Nome. Use 'Alterar'.")
            return
            
        data = self.coletar_dados_form()
        try:
            result = self.collection.insert_one(data)
            self.documento_id_carregado = result.inserted_id
            messagebox.showinfo("Sucesso", "Local salvo com sucesso!")
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
            messagebox.showwarning("Atenção", "Consulte um local antes de alterar.")
            return
            
        data = self.coletar_dados_form()
        try:
            self.collection.update_one(
                {"_id": self.documento_id_carregado},
                {"$set": data}
            )
            messagebox.showinfo("Sucesso", "Local alterado com sucesso!")
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
        nome = self.entry_nome_local.get()
        if not nome:
            messagebox.showwarning("Atenção", "Digite o 'Nome Local' para consultar.")
            return

        try:
            data = self.collection.find_one({"nome_local": nome})
            if data:
                self.popular_form(data)
            else:
                messagebox.showinfo("Não encontrado", "Nenhum local encontrado com este Nome.")
                self.limpar_campos()
                self.entry_nome_local.insert(0, nome)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar: {e}")

    def excluir(self):
        if not self.documento_id_carregado:
            messagebox.showwarning("Atenção", "Consulte um local antes de excluir.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este local?"):
            try:
                self.collection.delete_one({"_id": self.documento_id_carregado})
                messagebox.showinfo("Sucesso", "Local excluído.")
                try:
                    self.carregar_lista()
                except Exception:
                    pass
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")