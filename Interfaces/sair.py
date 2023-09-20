import tkinter as tk
from PIL import Image, ImageTk
from interfaces_mixins.centralizar_tela import Centralizar
from interfaces_mixins.botao_liga_desliga import Button_OnOff
class Sair(Centralizar):
    def __init__(self, master, janela_pai):
        self.janela_pai = janela_pai
        self.janela_sair = master
        self.janela_sair.grab_set()
        self.janela_sair.title("Sair?")
        self.janela_sair.resizable(False, False)
        self.janela_sair.overrideredirect(True)
        self.janela_sair.config(bg="#383033")
        Centralizar(self.janela_sair,428,136)
        #Frames ========================================================================================================
        self.frame_pergunta = tk.Frame(self.janela_sair, bg="#383033")
        self.frame_botoes   = tk.Frame(self.janela_sair, bg="#383033")

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
        self.janela_pai.destroy()

    def nao(self):
        self.janela_sair.destroy()
