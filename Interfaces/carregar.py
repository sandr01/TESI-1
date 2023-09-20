import tkinter as tk
from PIL import Image, ImageTk
from interfaces_mixins.centralizar_tela import Centralizar
from interfaces_mixins.botao_liga_desliga import Button_OnOff
import banco_de_dados.bd_plantas as bd
banco_de_dados = "../banco_de_dados/save.db"

class Carregar:
    def __init__(self, master, janela_pai):
        self.janela_pai = janela_pai
        self.janela_carregar = master
        self.janela_carregar.grab_set()
        self.janela_carregar.title("Carregar?")
        self.janela_carregar.resizable(False, False)
        self.janela_carregar.overrideredirect(True)
        self.janela_carregar.config(bg="#383033")

        Centralizar(self.janela_carregar, 200, 120)
        # Frames ========================================================================================================
        self.btn_save1 = Button_OnOff(self.janela_carregar, "1", '../src/botões/botao_save1', "#383033", lambda: self.carregar("1"))
        self.btn_save2 = Button_OnOff(self.janela_carregar, "2", '../src/botões/botao_save2', "#383033", lambda: self.carregar("2"))
        self.btn_save3 = Button_OnOff(self.janela_carregar, "3", '../src/botões/botao_save3', "#383033", lambda: self.carregar("3"))
        # Sets ==========================================================================================================

        self.btn_save1.pack()
        self.btn_save2.pack()
        self.btn_save3.pack()

    def carregar(self, qual):
        bd.set_save_atual(banco_de_dados,qual)
        self.janela_carregar.destroy()
