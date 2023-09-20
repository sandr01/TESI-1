
class Txt_Para_Lista():
    def __init__(self):
        pass

    def get_lista(self, diretorio):
        with  open(f'{diretorio}', 'a') as arquivo1:
            arquivo1.close()
        with  open(f'{diretorio}', 'r') as arquivo2:
            conteudo = arquivo2.read()
            lista_conteudo = conteudo.split("\n")
            arquivo2.close()
            lista_conteudo = lista_conteudo[:-1]
        return lista_conteudo

    def set_lista(self, diretorio, novo_texto):
        with  open(f'{diretorio}', 'a') as arquivo:
            arquivo.write(novo_texto+"\n")
            arquivo.close()