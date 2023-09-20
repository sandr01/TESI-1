import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from interfaces_mixins.botao_liga_desliga import Button_OnOff
import banco_de_dados.bd_plantas as bd
from interfaces_mixins.str_para_imagem import Str_Para_Imagem
from Comprar_loja import Sair_loja
from interfaces_mixins.centralizar_tela import Centralizar

class Janela_Loja(Str_Para_Imagem):

    def __init__(self, master, save_atual, janela_pai, botoes_carrinho_principal):
        self.janela_pai = janela_pai
        self.cor_fundo = "#383033"
        self.cor_texto = "#f6f5eb"
        self.banco_de_dados = "../banco_de_dados/save.db"
        self.save_atual = save_atual
        self.janela_loja = master
        self.janela_loja.title("Lolja")
        self.janela_loja.grab_set()
        self.janela_loja.resizable(False, False)
        self.janela_loja.config(bg=self.cor_fundo)
        self.botoes_carrinho = []
        self.botoes_carrinho_principal = botoes_carrinho_principal
        self.total_compra = 0
        self.janela_loja.lift()
        Centralizar(self.janela_loja, 790, 435)

        #Ibagens
        #Frames
        self.frame_cabeca   = tk.Frame(self.janela_loja, bg=self.cor_fundo, bd=0)
        self.frame_TreeView = tk.Frame(self.janela_loja, bg=self.cor_fundo, bd=0)

        #Label_frame_carrinho
        self.label_frame_carrinho = tk.LabelFrame(self.janela_loja, text='Carrinho', fg=self.cor_texto, bg=self.cor_fundo)
        #Frames
        self.frame_carrinho   = tk.Frame(self.janela_loja         , bg=self.cor_fundo)
        self.frame_inventario = tk.Frame(self.label_frame_carrinho, bg=self.cor_fundo)
        self.frame_comprar    = tk.Frame(self.label_frame_carrinho, bg=self.cor_fundo)

        #LabelFrame_Valor
        self.label_frame_valor = tk.LabelFrame(self.frame_comprar, text='valor total',fg=self.cor_texto, bg=self.cor_fundo)

        #Butones
        self.btn_plantas     = Button_OnOff(self.frame_cabeca, "Plantas", '../src/botões/botao_plantas', self.cor_fundo, lambda:self.atualizar_tvw_plantas(self.lista_plantas_tupla))
        self.btn_ferramentas = Button_OnOff(self.frame_cabeca, "Ferramentas", '../src/botões/botao_ferramentas', self.cor_fundo, lambda:self.atualizar_tvw_ferramentas(self.lista_ferramentas_tupla))
        self.btn_adubos      = Button_OnOff(self.frame_cabeca, "Adubos...", '../src/botões/botao_fertilizantes', self.cor_fundo, lambda:self.atualizar_tvw_adubos(self.lista_adubos_tupla))

        self.btn_comprar     = Button_OnOff(self.frame_comprar, "Comprar"  , '../src/botões/botao_comprar', self.cor_fundo, self.comprar)
        self.btn_voltar = Button_OnOff(self.frame_comprar, "Voltar", '../src/botões/botao_sair', self.cor_fundo, self.sair)

        #Label
        self.lbl_vazio = tk.Label(self.frame_carrinho, text="..................")
        self.lbl_vazio2 = tk.Label(self.frame_inventario, text="...........")

        Nome_imagem = self.get_imagem_dinheiro('0', "total_a_pagar")
        self.imagem = ImageTk.PhotoImage(Image.open(Nome_imagem + "_off.png"))
        self.lbl_valor_t = tk.Label(self.label_frame_valor, image=self.imagem, text="1000:", fg=self.cor_texto, bg=self.cor_fundo)
        self.lbl_carrinho = tk.LabelFrame(self.label_frame_carrinho, text="car")
        self.lbl_valor_t.image = self.imagem

        # Scrollbar
        self.scroll = ttk.Scrollbar(self.frame_TreeView)

        #Estilo
        style = ttk.Style()             #Instãncia de um objeto style
        style.theme_use("clam")
        style.configure("Treeview"        , background = self.cor_fundo, foreground = self.cor_texto, rowheight = 25, fieldbackground = self.cor_fundo)
        style.configure('Treeview.Heading', background = self.cor_fundo, foreground = self.cor_texto)
        #Mudar a cor da seleção
        style.map("Treeview", background=[('selected', 'green')])

        #TreeView
        colunas = ['#', 'produto', 'estagios', 'preço', 'qualidade']
        self.Treeview_loja = ttk.Treeview(self.frame_TreeView, show='headings', columns=colunas, height=10, selectmode='browse', yscrollcommand=self.scroll.set)

        #Cabeçalho
        self.Treeview_loja.heading('#', text="#")
        self.Treeview_loja.heading('produto', text="Produto")
        self.Treeview_loja.heading('estagios', text="Estágios")
        self.Treeview_loja.heading('preço', text="Preço")
        self.Treeview_loja.heading('qualidade', text="Qualidade")


        self.Treeview_loja.column('#', width=78)
        self.Treeview_loja.column('produto', width=350)
        self.Treeview_loja.column('estagios', width=120)
        self.Treeview_loja.column('preço', width=280)
        self.Treeview_loja.column('qualidade', width=280)

        # Insert image to #

        self.scroll.config(command=self.Treeview_loja.yview)
        self.lista_plantas_tupla = bd.consultar_tabela(self.banco_de_dados, "plantas")
        self.lista_ferramentas_tupla = bd.consultar_tabela(self.banco_de_dados, "ferramentas")
        self.lista_adubos_tupla = bd.consultar_tabela(self.banco_de_dados, "adubos")

        self.save_atual = bd.get_save_atual(self.banco_de_dados)

        self.lista_p = []
        self.lista_f = []
        self.lista_a = []
        self.lista_index = []
        self.lista_imagens = []
        self.lista_nome = []

        for i in self.lista_plantas_tupla:
            self.lista_p.append(i[1])
        for i in self.lista_ferramentas_tupla:
            self.lista_f.append(i[1])
        for i in self.lista_adubos_tupla:
            self.lista_a.append(i[1])


        self.atualizar_tvw_plantas(self.lista_plantas_tupla)
        #Sets ==========================================================================================================
        #Frames
        self.frame_cabeca.pack()
        self.frame_TreeView.pack()
        self.frame_carrinho.pack(expand=True, fill=tk.X)

        self.frame_inventario.pack(expand=True, fill=tk.X, side=tk.LEFT)
        self.frame_comprar.pack(side=tk.RIGHT)
        self.label_frame_carrinho.pack()
        self.label_frame_valor.pack()
        self.label_frame_carrinho.pack()

        #frame_cabeça
        self.btn_plantas.grid(row=0, column=0)
        self.btn_ferramentas.grid(row=0, column=1)
        self.btn_adubos.grid(row=0, column=2)

        #frame_TreeView
        self.Treeview_loja.pack(side=tk.LEFT)
        self.scroll.pack(side=tk.RIGHT, expand=True, fill=tk.Y)

        #frame_carrinho
        self.lbl_carrinho.pack()
        # self.lbl_vazio.grid(row=0, column=1)
        self.lbl_valor_t.pack(side=tk.TOP)

        #frame_inventario
        self.inventario = bd.get_inventario(self.banco_de_dados, self.save_atual)
        bd.gerar_carrinho(self.banco_de_dados, self.inventario)
        self.carrinho = bd.get_carrinho(self.banco_de_dados)
        self.por_slots()

        # self.lbl_vazio2.pack()
        # self.btn_inventario1.grid(row=0, column=0)
        # self.btn_inventario2.grid(row=0, column=1)
        # self.btn_inventario3.grid(row=0, column=2)
        self.btn_comprar.pack(side=tk.BOTTOM)
        self.btn_voltar.pack(side=tk.BOTTOM)

        #Binds
        self.Treeview_loja.bind("<<TreeviewSelect>>", self.clicou)

    #Funções do bagulho doido
    def atualizar_tvw_plantas(self, lista):
        self.Treeview_loja.column('preço', width=280)
        self.Treeview_loja.column('produto', width=240)
        self.Treeview_loja["displaycolumns"] =  ['#', 'produto', 'estagios', 'preço']
        for i in self.Treeview_loja.get_children():
            self.Treeview_loja.delete(i)
        dados = bd.consultar_tabela(self.banco_de_dados, "plantas")
        for tupla in dados:
            self.Treeview_loja.insert('', tk.END, values=tupla)

    def atualizar_tvw_ferramentas(self, lista):
        self.Treeview_loja.column('produto', width=240)
        self.Treeview_loja.column('preço', width=120)
        self.Treeview_loja["displaycolumns"] =  ['#', 'produto', 'preço','qualidade']
        for i in self.Treeview_loja.get_children():
            self.Treeview_loja.delete(i)
        dados = bd.consultar_tabela(self.banco_de_dados, "ferramentas")
        for tupla in dados:
            self.Treeview_loja.insert('', tk.END, values=tupla)

    def atualizar_tvw_adubos(self, lista):
        self.Treeview_loja.column('preço', width=120)
        self.Treeview_loja.column('produto', width=240)
        self.Treeview_loja["displaycolumns"] =  ['#', 'produto', 'preço','qualidade']
        for i in self.Treeview_loja.get_children():
            self.Treeview_loja.delete(i)
        dados = bd.consultar_tabela(self.banco_de_dados, "adubos")
        for tupla in dados:
            self.Treeview_loja.insert('', tk.END, values=tupla)

    def por_slots(self):
        for i in self.carrinho:
            icone = "../src/icones/" + i[1] + "_icone"
            if(i[1] != 'nada'):
                botao = Button_OnOff(self.frame_inventario, i[1], "../src/icones/nao_disponivel_icone", self.cor_fundo, 'doNothing', 'normal', True)
                self.botoes_carrinho.append(botao)
            else:
                botao = Button_OnOff(self.frame_inventario, i[1], icone, self.cor_fundo, lambda aux=i:self.desclicou(aux))
                self.botoes_carrinho.append(botao)

        for i in range(len(self.carrinho)):
            self.botoes_carrinho[i].grid(row=0, column=i)

    def clicou(self, event):
        self.selecionado = self.Treeview_loja.selection()
        lista = (self.Treeview_loja.item(self.selecionado))
        nome = lista['values'][1]
        preco = lista['values'][3]
        status = bd.set_carrinho(self.banco_de_dados, nome)
        if( status == "cheio"):
            messagebox.showinfo('Aviso', 'Carrinho enchido')
        else:
            botao = self.botoes_carrinho[int(status) - 1]
            self.lista_index.append(self.botoes_carrinho.index(botao) +1)

            if(nome in self.lista_p):
                nome_imagem = bd.get_icone_produto(self.banco_de_dados, "plantas", nome)
            elif (nome in self.lista_f):
                nome_imagem = bd.get_icone_produto(self.banco_de_dados, "ferramentas", nome)
            else:
                nome_imagem = bd.get_icone_produto(self.banco_de_dados, "adubos", nome)
            botao.set_imagem(nome_imagem)
            self.total_compra += preco
            imagem_dinheiro = self.get_imagem_dinheiro(f'{self.total_compra}', "total_a_pagar")
            imagem = ImageTk.PhotoImage(Image.open(imagem_dinheiro + "_off.png"))
            self.lista_imagens.append(nome_imagem)
            self.lista_nome.append(nome)
            self.lbl_valor_t.config(image=imagem)
            self.lbl_valor_t.image = imagem
            botao.config(text=nome)

    def desclicou(self, o_que):
        print(o_que)
        posicao = o_que[0]
        bd.atualizar(self.banco_de_dados, "carrinho", posicao, ['produto'],['nada'], True)
        botao = self.botoes_carrinho[posicao]
        botao.set_imagem('nada_icone_off.png')
        botao.config(text='nada')


    def comprar(self):
        self.top_sair = tk.Toplevel(self.janela_loja)
        Sair_loja(self.top_sair, self.janela_loja, self.janela_pai, self.lista_index, self.botoes_carrinho_principal, self.lista_imagens, self.lista_nome, self.save_atual, self.total_compra)

    def sair(self):
        self.top_sair = tk.Toplevel(self.janela_loja)
        Sair_loja(self.top_sair, self.janela_loja, self.janela_pai, self.lista_index, self.botoes_carrinho_principal,
                  self.lista_imagens, self.lista_nome, self.save_atual, self.total_compra)