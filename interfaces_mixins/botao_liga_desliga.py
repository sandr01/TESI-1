import tkinter as tk
from PIL         import Image, ImageTk

class Button_OnOff(tk.Button):

    def __init__(self, que_frame: object, texto: str, diretorio_sem_on_ou_off: str, cor_fundo: str, comando = 'donothing', estado="normal", tirar_animacao=False):
        '''
        Cria um botão em que a imagem muda para dois estados ao passar o cursor por cima\n
        Requer 1 uma imagem que tenha uma variação ativa\n
        Exige um objeto <que_frame> do tipo tkinter.Frame\n
        Exige uma string <texto> para salvar no texto do botão\n
        Exige uma string <diretorio_sem_on_ou_off> contendo o diretorio da imagem, deve seguir as seguintes regras:
            -O nome da imagem deve ser 'nome_icone_off.png', '_off' é obrigatorio\n
            -Ao passar a imagem como parâmetro só mande até antes de '_off':
                -Diretorio: '../src/nada_icone_off.png'\n
                -Parâmetro  '../src/nada_icone_off.png'
        Exige uma string <cor_fundo> contendo a cor do fundo;\n
        Uma função opcional <comando> que será atribuido ao command do botao, padrão é 'donothing';\n
        Uma string opcional informando o estado do botao: active, disabled, or normal, normal por padrão;\n
        Um boleano informando se deseja remover a animação do botao, False por padrão.
        '''
        self.que_frame               = que_frame
        self.texto                   = texto
        self.diretorio_sem_on_ou_off = diretorio_sem_on_ou_off
        self.cor_fundo               = cor_fundo
        self.comando                 = comando
        self.estado                  = estado
        self.imagem_off = ImageTk.PhotoImage(Image.open(self.diretorio_sem_on_ou_off + '_off.png'))
        self.imagem_on  = ImageTk.PhotoImage(Image.open(self.diretorio_sem_on_ou_off + '_on.png'))

        tk.Button.__init__(self, master=self.que_frame)
        self['bg']               = self.cor_fundo
        self['text']             = self.texto
        self['command']          = self.comando
        self['image']            = self.imagem_off
        self['bd']               = 0
        self['activebackground'] = self.cor_fundo
        self['state']            = self.estado

        if(tirar_animacao):
            self['relief']       = 'sunken'
        self.bind("<Enter>", self.mudar_imagem_on)
        self.bind("<Leave>", self.mudar_imagem_off)

    def mudar_imagem_on(self, event):
        self.config(image=self.imagem_on)
        self.image = self.imagem_on

    def mudar_imagem_off(self, event):
        self.config(image=self.imagem_off)
        self.image = self.imagem_off

    def set_imagem(self, nome_img):
        imagem_off = ImageTk.PhotoImage(Image.open('../src/icones/'+ nome_img))
        imagem_on = nome_img.replace("off", "on")
        self.config(image=imagem_off)
        self.image = imagem_off
        self.imagem_off = ImageTk.PhotoImage(Image.open('../src/icones/'+ nome_img))
        self.imagem_on = ImageTk.PhotoImage(Image.open('../src/icones/'+ imagem_on))
