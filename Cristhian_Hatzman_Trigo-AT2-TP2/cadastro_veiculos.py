import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, filedialog, PhotoImage
from database import conectar_db
from bson.objectid import ObjectId
from PIL import Image, ImageTk

class TelaVeiculos:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Veículos")
        self.root.geometry("700x650")
        self.root.configure(bg="#f0f0f0") 

        self.db = conectar_db()
        if self.db is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao MongoDB.")
            self.root.destroy()
            return
        self.collection = self.db['veiculos']
        
        self.documento_id_carregado = None
        self.caminho_imagem = tk.StringVar()
        
        
        frame_form = ttk.Frame(self.root, padding=10)
        frame_form.pack(pady=10, padx=10, fill='x')

        frame_img = ttk.Frame(self.root, padding=10)
        frame_img.pack(pady=10, padx=10, fill='x')

        frame_botoes = ttk.Frame(self.root, padding=10)
        frame_botoes.pack(pady=10, fill='x')

        frame_listagem = ttk.Frame(self.root, padding=10)
        frame_listagem.pack(padx=10, fill='both', expand=True)

        ttk.Label(frame_form, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_codigo = ttk.Entry(frame_form, width=10)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(frame_form, text="Nome Veículo:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_nome_veiculo = ttk.Entry(frame_form, width=30)
        self.entry_nome_veiculo.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        ttk.Label(frame_form, text="Modelo:").grid(row=1, column=2, padx=5, pady=5, sticky='w')
        self.entry_modelo = ttk.Entry(frame_form, width=20)
        self.entry_modelo.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(frame_form, text="Placa:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_placa = ttk.Entry(frame_form, width=15)
        self.entry_placa.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(frame_form, text="Marca:").grid(row=2, column=2, padx=5, pady=5, sticky='w')
        marcas = ["Chevrolet", "Fiat", "Ford", "Volkswagen", "Renault", "Suzuki", "Outra"]
        self.combo_marca = ttk.Combobox(frame_form, values=marcas, width=18)
        self.combo_marca.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        self.var_utilitario = tk.StringVar(value="Não")
        ttk.Label(frame_form, text="Utilitário:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        frame_radio_util = ttk.Frame(frame_form)
        frame_radio_util.grid(row=3, column=1, sticky='w')
        ttk.Radiobutton(frame_radio_util, text="Sim", variable=self.var_utilitario, value="Sim").pack(side='left')
        ttk.Radiobutton(frame_radio_util, text="Não", variable=self.var_utilitario, value="Não").pack(side='left', padx=10)

        self.label_imagem = ttk.Label(frame_img, text="[Sem Imagem]", relief="solid", width=25, anchor='center')
        self.label_imagem.pack(side='left', padx=10)

        btn_escolher_img = ttk.Button(frame_img, text="Escolher Imagem", command=self.escolher_imagem)
        btn_escolher_img.pack(side='left', padx=10, anchor='center')

        self.img_cadastrar = PhotoImage(file="icones/salvar.png")
        self.img_alterar = PhotoImage(file="icones/alterar.png")
        self.img_excluir = PhotoImage(file="icones/excluir.png")

        btn_salvar = ttk.Button(frame_botoes, text="Salvar", image=self.img_cadastrar, compound='left', command=self.salvar)
        btn_salvar.pack(side='left', padx=5)
        btn_alterar = ttk.Button(frame_botoes, text="Alterar", image=self.img_alterar, compound='left', command=self.alterar)
        btn_alterar.pack(side='left', padx=5)
        btn_consultar = ttk.Button(frame_botoes, text="Consultar", command=self.consultar)
        btn_consultar.pack(side='left', padx=5)
        btn_excluir = ttk.Button(frame_botoes, text="Excluir", image=self.img_excluir, compound='left', command=self.excluir)
        btn_excluir.pack(side='left', padx=5)
        btn_limpar = ttk.Button(frame_botoes, text="Limpar", command=self.limpar_campos)
        btn_limpar.pack(side='left', padx=5)
        btn_sair = ttk.Button(frame_botoes, text="Sair", command=self.root.destroy)
        btn_sair.pack(side='right', padx=10)

        cols = ("codigo", "nome_veiculo", "placa", "marca")
        self.tree = ttk.Treeview(frame_listagem, columns=cols, show='headings', height=6)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=140)

        vsb = ttk.Scrollbar(frame_listagem, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True, padx=(0,5))
        vsb.pack(side='left', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.on_tree_double_click)

        # carregar lista inicial
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
            "nome_veiculo": self.entry_nome_veiculo.get(),
            "placa": self.entry_placa.get(),
            "utilitario": self.var_utilitario.get(),
            "modelo": self.entry_modelo.get(),
            "marca": self.combo_marca.get(),
            "caminho_imagem": self.caminho_imagem.get(),
        }

    def popular_form(self, data):
        self.entry_codigo.delete(0, 'end'); self.entry_codigo.insert(0, data.get("codigo", ""))
        self.entry_nome_veiculo.delete(0, 'end'); self.entry_nome_veiculo.insert(0, data.get("nome_veiculo", ""))
        self.entry_placa.delete(0, 'end'); self.entry_placa.insert(0, data.get("placa", ""))
        self.var_utilitario.set(data.get("utilitario", "Não"))
        self.entry_modelo.delete(0, 'end'); self.entry_modelo.insert(0, data.get("modelo", ""))
        self.combo_marca.set(data.get("marca", ""))
        
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
            # limpar tree
            for i in self.tree.get_children():
                self.tree.delete(i)

            for doc in self.collection.find().sort("codigo", 1):
                codigo = doc.get("codigo", "")
                nome = doc.get("nome_veiculo", "")
                placa = doc.get("placa", "")
                marca = doc.get("marca", "")
                iid = str(doc.get("_id"))
                self.tree.insert('', 'end', iid=iid, values=(codigo, nome, placa, marca))
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
                placa = vals[2]
                doc = self.collection.find_one({"placa": placa})
                if doc:
                    self.popular_form(doc)

    def on_tree_double_click(self, event):
        self.on_tree_select(event)

    def salvar(self):
        placa = self.entry_placa.get()
        if not placa:
            messagebox.showwarning("Atenção", "A 'Placa' é obrigatória para salvar.")
            return

        if self.collection.find_one({"placa": placa}):
            messagebox.showerror("Erro", "Já existe um veículo com esta Placa. Use 'Alterar'.")
            return
            
        data = self.coletar_dados_form()
        try:
            result = self.collection.insert_one(data)
            self.documento_id_carregado = result.inserted_id
            messagebox.showinfo("Sucesso", "Veículo salvo com sucesso!")
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
            messagebox.showwarning("Atenção", "Consulte um veículo antes de alterar.")
            return
            
        data = self.coletar_dados_form()
        try:
            self.collection.update_one(
                {"_id": self.documento_id_carregado},
                {"$set": data}
            )
            messagebox.showinfo("Sucesso", "Veículo alterado com sucesso!")
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
        
        placa = self.entry_placa.get()
        if not placa:
            messagebox.showwarning("Atenção", "Digite a 'Placa' para consultar.")
            return

        try:
            data = self.collection.find_one({"placa": placa})
            if data:
                self.popular_form(data)
                try:
                    _id = data.get("_id")
                    if _id:
                        self.tree.selection_set(str(_id))
                        self.tree.see(str(_id))
                except Exception:
                    pass
            else:
                messagebox.showinfo("Não encontrado", "Nenhum veículo encontrado com esta Placa.")
                self.limpar_campos()
                self.entry_placa.insert(0, placa)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar: {e}")

    def excluir(self):
        if not self.documento_id_carregado:
            messagebox.showwarning("Atenção", "Consulte um veículo antes de excluir.")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este veículo?"):
            try:
                self.collection.delete_one({"_id": self.documento_id_carregado})
                messagebox.showinfo("Sucesso", "Veículo excluído.")
                try:
                    self.carregar_lista()
                except Exception:
                    pass
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {e}")