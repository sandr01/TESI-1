
class Centralizar():
    def __init__(self, que_janela,largura, altura):
        self.que_janela = que_janela
        self.largura    = largura
        self.altura     = altura

        l = largura
        a = altura
        l_tela = self.que_janela.winfo_screenwidth()
        a_tela = self.que_janela.winfo_screenheight()

        x = (l_tela / 2) - (l / 2)
        y = (a_tela / 2) - (a / 2)

        self.que_janela.geometry(f'{l}x{a}+{int(x)}+{int(y)}')
