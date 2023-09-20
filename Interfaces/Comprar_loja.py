import tkinter as tk
from PIL import Image, ImageTk
from interfaces_mixins.centralizar_tela import Centralizar
from interfaces_mixins.botao_liga_desliga import Button_OnOff
import banco_de_dados.bd_plantas as bd
from interfaces_mixins.str_para_imagem import Str_Para_Imagem

class Sair_loja(Centralizar, Str_Para_Imagem):
    def __init__(self, master, janela_loja, janela_pai, lista_index, carrinho_principal, lista_imagens, lista_nomes, save_atual, total_compra):
        self.janela_loja = janela_loja
        self.janela_pai = janela_pai
        self.janela_comprar = master
        self.banco_de_dados = "../banco_de_dados/save.db"
        self.janela_comprar.grab_set()
        self.janela_comprar.title("Sair?")
        self.janela_comprar.resizable(False, False)
        self.janela_comprar.overrideredirect(True)
        self.janela_comprar.config(bg="#383033")
        self.save_atual = save_atual
        self.lista_index = lista_index
        self.lista_img = lista_imagens
        self.lista_nomes = lista_nomes
        self.total_compra = total_compra
        print(lista_nomes)
        self.carrinho_principal = carrinho_principal
        Centralizar(self.janela_comprar, 428, 136)
        self.janela_pai.lift()
        self.janela_loja.lift()
        self.janela_comprar.lift()
        #Frames ========================================================================================================
        self.frame_pergunta = tk.Frame(self.janela_comprar, bg="#383033")
        self.frame_botoes   = tk.Frame(self.janela_comprar, bg="#383033")

        #Labels ========================================================================================================
        self.img_pergunta = ImageTk.PhotoImage(Image.open ('../src/texto_sair.png'))
        self.lbl_pergunta = tk.Label(self.frame_pergunta, image=self.img_pergunta, bg="#383033")
        self.lbl_pergunta.image = self.img_pergunta

        self.btn_sim = Button_OnOff(self.frame_botoes,"sim",'../src/botões/botao_sim', "#383033", self.sim)
        self.btn_nao = Button_OnOff(self.frame_botoes,"nao",'../src/botões/botao_nao', "#383033", self.nao)

        #Sets ==========================================================================================================
        self.frame_pergunta.pack()
        self.frame_botoes.pack()

        #Frame Perguntas
        self.lbl_pergunta.pack()

        #Frame Botões
        self.btn_sim.pack(side=tk.LEFT,ipadx=10)
        self.btn_nao.pack(side=tk.LEFT,ipadx=10)

    def sim(self):
        print(self.total_compra)
        for i, j in enumerate(self.lista_index):
            bd.alterar_espaco(self.banco_de_dados, self.save_atual, j, self.lista_nomes[i])

        bd.sacar(self.banco_de_dados, self.save_atual, self.total_compra)
        self.janela_loja.destroy()
        self.janela_pai.lift()

    def nao(self):
        self.janela_comprar.destroy()
        self.janela_pai.lift()
