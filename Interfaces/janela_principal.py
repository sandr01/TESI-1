import re
import tkinter as tk
from tkinter import messagebox, ttk
import banco_de_dados.bd_plantas as bd
from interfaces_mixins.planta_interface   import Planta_Interface
from interfaces_mixins.botao_liga_desliga import Button_OnOff
from interfaces_mixins.centralizar_tela   import Centralizar
from interfaces_mixins.txt_para_lista     import Txt_Para_Lista
from interfaces_mixins.str_para_imagem    import Str_Para_Imagem
from PIL         import Image, ImageTk
from janela_loja import Janela_Loja
from carregar    import Carregar
from sair        import Sair

class Janela_Principal(Planta_Interface, Centralizar, Txt_Para_Lista, Str_Para_Imagem):
    funcoes_janela = True
    funcoes_planta = True

    def __init__(self, master):
        self.banco_de_dados = "../banco_de_dados/save.db"
        # Cores
        self.cor_fundo = "#383033"
        self.cor_texto = "#f6f5eb"
        super().__init__()
        self.janela_principal = master
        self.janela_principal.update_idletasks()
        self.janela_principal.overrideredirect(True)
        self.janela_principal.title("Janela Principal")
        self.janela_principal.resizable(False, False)
        self.janela_principal.config(bg=self.cor_fundo)
        #Centralizando
        Centralizar(self.janela_principal, 630, 535)

        self.borda = tk.Frame(self.janela_principal, bg=self.cor_texto, bd=9, width=630, height=535)

        # Imagens =======================================================================================================
        # Inventario
        self.img_nada       = ImageTk.PhotoImage(Image.open ('../src/nada.png'))
        self.img_texto      = ImageTk.PhotoImage(Image.open ('../src/caixa_texto.png'))
        self.img_inventario = ImageTk.PhotoImage(Image.open ('../src/icones/inventario_icone_off.png'))
        self.img_vazio      = ImageTk.PhotoImage(Image.open ('../src/icones/inventario_icone_off.png'))

        # Interface ----------------------------------------------------------------------------------------------------
        # Frames
        self.frame_1   = tk.Frame(self.borda, bg=self.cor_fundo)
        self.frame_2   = tk.Frame(self.borda, bg=self.cor_fundo)

        self.frame_2_1 = tk.Frame(self.frame_2, bg=self.cor_fundo)
        self.frame_2_2 = tk.Frame(self.frame_2, bg=self.cor_fundo)
        self.frame_2_3 = tk.Frame(self.frame_2, bg=self.cor_fundo)

        #Variaves
        self.save_atual = bd.get_save_atual(self.banco_de_dados)
        self.lista_lista_plantas = bd.consultar_coluna(self.banco_de_dados, "plantas", "nome")
        self.lista_plantas = []
        for i in self.lista_lista_plantas:
            self.lista_plantas.append(i[0])

        self.item_selecionado = ''
        self.botoes_inventario = []

        self.historico_atual = "../banco_de_dados/historico_"f'{self.save_atual}'".txt"
        self.lista_historico = self.get_lista(self.historico_atual)

        self.lbl_debug = tk.Label(self.borda, text='', fg= self.cor_texto, bg=self.cor_fundo)

        # Label
        self.lbl_planta  = tk.Label(self.frame_1, image=self.img_nada, bg=self.cor_fundo)
        self.borda_texto = tk.Frame(self.frame_1, bg=self.cor_texto, bd=5)
        self.txa_texto   = tk.Text (self.borda_texto, width=48, height=6, bg=self.cor_fundo, fg=self.cor_texto, bd=0, selectbackground=self.cor_fundo)
        self.txa_texto['state'] = "disabled"
        self.inserir_texto(self.lista_historico)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Vertical.TScrollbar", background=self.cor_fundo, bordercolor=self.cor_fundo, arrowcolor=self.cor_texto)

        self.scrollbar1 = ttk.Scrollbar(self.borda_texto, command=self.txa_texto.yview)
        self.txa_texto.configure(yscrollcommand=self.scrollbar1.set)

        #Botões
        self.btn_carregar = Button_OnOff(self.frame_2_1, "carregar", "../src/botões/botao_carregar", self.cor_fundo, self.carregar)
        self.btn_sair     = Button_OnOff(self.frame_2_1, "sair"    , "../src/botões/botao_sair"    , self.cor_fundo, self.sair)

        self.btn_comprar  = Button_OnOff(self.frame_2_3, "comprar" , "../src/botões/botao_comprar" , self.cor_fundo, self.abrir_loja)
        self.btn_vender   = Button_OnOff(self.frame_2_3, "vender"  , "../src/botões/botao_vender"  , self.cor_fundo, self.vender)

        self.saldo_atual = bd.get_saldo(self.banco_de_dados, self.save_atual)
        imagem = self.get_imagem_dinheiro(self.saldo_atual, 'dinheiro')
        self.btn_dinheiro = Button_OnOff(self.frame_2_3, "dinheiro" ,imagem , self.cor_fundo, 'donothing', 'normal',True)

        # Sets
        self.borda.pack(expand=True, fill=tk.BOTH)
        self.frame_1.grid(row=0, column=0, sticky='n,s,w,e')
        self.frame_2.grid(row=0, column=1, sticky='n,s,w,e')

        #Label_Frame_1
        self.lbl_planta.grid (row=0, column=0)
        self.borda_texto.grid(row=1, column=0, padx=(5,0) , pady=(0,5))
        self.txa_texto.pack(side=tk.LEFT)
        self.scrollbar1.pack(side=tk.RIGHT,fill=tk.BOTH)
        # self.lbl_debug.grid (row=2, column=0)

        # Label_Frame_2
            #Label_Frame_2_1
        self.frame_2_1.pack   (expand=True, fill=tk.X)
        self.btn_carregar.pack(expand=True, fill=tk.X)
        self.btn_sair.pack    (expand=True, fill=tk.X)

            #Label_Frame_2_2
        self.frame_2_2.pack(expand=True, fill=tk.X)
        self.por_inventario()

            # Label_Frame_2_3
        self.frame_2_3.pack   (expand=True, fill=tk.X)
        self.btn_vender.pack  (expand=True, fill=tk.X)
        self.btn_comprar.pack (expand=True, fill=tk.X)

        self.btn_dinheiro.pack(expand=True, fill=tk.X)

        self.atualizar_imagem()
        self.borda.bind("<B1-Motion>", self.mover_tela)
        self.borda.bind("<Button-1>", self.pegar_posicao)

        # Main Loop
        self.janela_principal.mainloop()

    if(funcoes_janela):
        def recarregar(self):
            self.janela_principal.destroy()
            root = tk.Tk()
            Janela_Principal(root)

        def abrir_loja(self):
            self.top_loja = tk.Toplevel(self.janela_principal)
            Janela_Loja(self.top_loja, self.save_atual, self.janela_principal, self.botoes_inventario)
            self.janela_principal.wait_window(self.top_loja)
            self.saldo_atual = bd.get_saldo(self.banco_de_dados, self.save_atual)
            imagem = self.get_imagem_dinheiro(self.saldo_atual, 'dinheiro')
            imagem = ImageTk.PhotoImage(Image.open(imagem + "_off.png"))
            self.btn_dinheiro.config(image=imagem)
            self.btn_dinheiro.image = imagem
            bd.resetar_tabela(self.banco_de_dados,"carrinho")
            self.frame_2_2.destroy()
            self.botoes_inventario = []
            self.frame_2_2 = tk.Frame(self.frame_2, bg=self.cor_fundo)
            self.frame_2_1.pack(expand=True, fill=tk.X)
            self.frame_2_2.pack(expand=True, fill=tk.X)
            self.frame_2_3.pack(expand=True, fill=tk.X)
            self.por_inventario()
            self.recarregar()


        def carregar(self):
            self.top_carregar = tk.Toplevel(self.janela_principal)
            Carregar(self.top_carregar, self.janela_principal)
            self.janela_principal.wait_window(self.top_carregar)
            self.recarregar()

        def sair(self):
            self.top_sair = tk.Toplevel(self.janela_principal)
            Sair(self.top_sair, self.janela_principal)

        def atualizar_imagem(self):
            estagio_atual = bd.get_imagem_estagio_atual(self.banco_de_dados, self.save_atual)

            if(estagio_atual != None):
                imagem = ImageTk.PhotoImage(Image.open("../src/plantas/"f'{estagio_atual}'""))
                self.lbl_planta.config(image=imagem)
                self.lbl_planta.image = imagem
            else:
                imagem = ImageTk.PhotoImage(Image.open("../src/nada.png"))
                self.lbl_planta.config(image=imagem)
                self.lbl_planta.image = imagem

        def o_que_isso_faz(self, lista):
            planta = bd.get_planta_atual(self.banco_de_dados, self.save_atual)
            if lista == []:
                return False
            posicao = lista[0]
            self.valor = lista[1]
            self.item_selecionado = self.valor
            self.lbl_debug.config(text=self.valor)
            if self.valor == 'nada':
                return True
            if ('pá' in self.valor):
                self.reciclar(self.valor)
                return True
            if (self.valor in self.lista_plantas):
                self.plantar()
                return True
            if ('regador' in self.valor and planta != 'Nenhuma'):
                self.avancar_estagio()
                self.que_botao = self.botoes_inventario[posicao - 1]
                self.comando_anterior = self.que_botao.cget('command')
                self.que_botao.config(command=lambda txt_btn=[]: self.o_que_isso_faz(txt_btn))
                self.janela_principal.after(3000, self.timer_do_regador)

        def timer_do_regador(self):
            self.que_botao.config(command=self.comando_anterior)

        def por_inventario(self):
            inventario = bd.get_inventario(self.banco_de_dados, self.save_atual)
            for j in inventario:
                icone = "../src/icones/" + j[1] + "_icone"
                botao = Button_OnOff(self.frame_2_2, j[1], icone, self.cor_fundo,
                                     lambda txt_btn=j: self.o_que_isso_faz(txt_btn))
                self.botoes_inventario.append(botao)

            if (len(self.botoes_inventario) % 2 == 0):
                numero_linhas = len(self.botoes_inventario) / 2
            else:
                numero_linhas = int(len(self.botoes_inventario) / 2) + 1
            slot_it = 0
            for i in range(int(numero_linhas)):
                for j in range(2):
                    self.botoes_inventario[slot_it].grid(row=i, column=j)
                    slot_it += 1

        def pegar_posicao(self, event):
            global xwin
            global ywin
            xwin = event.x
            ywin = event.y

        def mover_tela(self, event):
            self.janela_principal.geometry(f'+{event.x_root - xwin}+{event.y_root - ywin}')

        def inserir_texto(self, que_texto: list):
            self.txa_texto['state'] = "normal"
            if(que_texto == []):
                return None
            if(len(que_texto) > 1):
                for i in que_texto:
                    self.txa_texto.insert(tk.END, i+'\n')
            else:
                self.txa_texto.insert(tk.END, que_texto[0]+'\n')
            self.txa_texto['state'] = "disabled"

    if(funcoes_planta):
        def plantar(self):
            #Verifica se nada esta selecionado
            if(self.item_selecionado == ''):
                messagebox.showinfo("Se liga heim D:<", "Nada foi selecionado para plantar!")
                return None
            #Verifica se o que ta selecionado é uma planta
            if(not(self.item_selecionado in self.lista_plantas) ):
                messagebox.showinfo("Se liga heim D:<", ""f'{self.item_selecionado.capitalize()}'" não é uma planta! D:<!")
                return None
            #Verifica se já tem algo plantado
            if(bd.ja_tem_algo_plantado(self.banco_de_dados, self.save_atual)):
                string = ""f'{bd.get_planta_atual(self.banco_de_dados, self.save_atual).capitalize()}'" já está plantado! D:<!"
                self.set_lista(self.historico_atual, string)
                self.inserir_texto([string])
                return None
            # Verifica se a planta existe
            if (bd.set_planta_atual(self.banco_de_dados, self.save_atual,self.item_selecionado)):
                self.atualizar_imagem()
                string =  "Você plantou "f'{bd.get_planta_atual(self.banco_de_dados, self.save_atual).capitalize()}'"!"
                self.set_lista(self.historico_atual, string)
                self.inserir_texto([string])
            else:
                messagebox.showinfo("Se liga heim D:<", "Ocorreu um erro ao tentar plantar!")

        def avancar_estagio(self):

            #Verifica se tem algo plantado
            if (not bd.ja_tem_algo_plantado(self.banco_de_dados, self.save_atual)):
                string = "Não tem nada plantado atualmente! D:<!"
                self.set_lista(self.historico_atual, string)
                self.inserir_texto([string])
                return None

            if(bd.atualizar_estagio(self.banco_de_dados, self.save_atual, 1)):
                string = ""f'{bd.get_planta_atual(self.banco_de_dados, self.save_atual).capitalize()}'" foi regado!"
                self.set_lista(self.historico_atual, string)
                self.inserir_texto([string])
                self.atualizar_imagem()
            else:
                string = ""f'{bd.get_planta_atual(self.banco_de_dados, self.save_atual).capitalize()}'" está no nível MAX!"
                self.set_lista(self.historico_atual, string)
                self.inserir_texto([string])

        def resetar(self):
            bd.resetar_planta(self.banco_de_dados, self.save_atual)
            self.atualizar_imagem()

        def reciclar(self, valor):
            if(bd.get_planta_atual(self.banco_de_dados, self.save_atual) != "Nenhuma"):
                string = "Você removeu a planta com "f'{valor}'"!"
                self.set_lista(self.historico_atual,string)
                self.inserir_texto([string])

            bd.resetar_save(self.banco_de_dados, self.save_atual)
            self.atualizar_imagem()

        def atualizar_inventario(self):
            self.frame_2_2.destroy()
            self.botoes_inventario = []
            self.frame_2_2 = tk.Frame(self.frame_2, bg=self.cor_fundo)
            self.frame_2_1.pack(expand=True, fill=tk.X)
            self.frame_2_2.pack(expand=True, fill=tk.X)
            self.frame_2_3.pack(expand=True, fill=tk.X)
            self.por_inventario()

        def vender(self):
            selecionado = self.item_selecionado
            for i in self.botoes_inventario:
                if(i.cget("text") == selecionado):
                    index = self.botoes_inventario.index(i)
                    bd.alterar_espaco(self.banco_de_dados, int(self.save_atual), f'{index +1}', 'nada', True)
                    self.atualizar_inventario()
                    break
                self.saldo_atual = bd.get_saldo(self.banco_de_dados, self.save_atual)
                imagem = self.get_imagem_dinheiro(f'{self.saldo_atual}', 'dinheiro')
                imagem = ImageTk.PhotoImage(Image.open(imagem + "_off.png"))
                self.btn_dinheiro.config(image=imagem)
                self.btn_dinheiro.image = imagem
            self.frame_2_2.destroy()
            self.botoes_inventario = []
            self.frame_2_2 = tk.Frame(self.frame_2, bg=self.cor_fundo)
            self.frame_2_1.pack(expand=True, fill=tk.X)
            self.frame_2_2.pack(expand=True, fill=tk.X)
            self.frame_2_3.pack(expand=True, fill=tk.X)
            self.por_inventario()
            self.recarregar()
