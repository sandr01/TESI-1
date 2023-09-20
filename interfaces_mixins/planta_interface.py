
class Planta_Interface():

    def __init__(self):
        pass

    def plantar(self):
        '''
        Cria uma tabela no save atual com a planta selecionada\n
        Se a tabela já existir é informado em uma mensagem e a criação é ignorada
        '''
        pass

    def avancar_estagio(self):
        '''
        Avança o estagio da planta em 1 estagio até no max o número
        '''
        pass

    def resetar(self):
        '''
        Reseta a planta atual do save <que_save> para o estagio 1
        '''
        pass

    def reciclar(self, valor):
        '''
        Remove a planta <que_planta> do save <que_save>
        '''
        pass