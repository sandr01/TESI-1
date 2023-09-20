import sqlite3
from sqlite3 import Error
save_teste = "../banco_de_dados/save.db"
#Metodo de conexão =====================================================================================================
def conexao_banco(caminho: str):
    '''
    Conecta a um banco de dados\n
    Retorna a conexão caso seja bem sucedido\n
    Retorna Error caso contrário
    '''
    quer_debug = False
    if(quer_debug):
        try:
            conexao = None
            conexao = sqlite3.connect(caminho)
            print('Conectado')
            return conexao
        except:
            print('Conexão broxou')
            return Error
    else:
        try:
            conexao = None
            conexao = sqlite3.connect(caminho)
            return conexao
        except:
            return Error

#Metodo de criar tabela ================================================================================================
def criar_tabela(que_banco: str, nome_da_tabela: str, chaves: list, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <nome_save> para nomear a tabela\n
    Exige uma lista de strings <chaves> contendo as chaves das colunas exceto o id primario\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Cria um tabela com nome <nome_da_tabela>\n
    É verificado se a tabela já existe no banco de dados
    Por padrão ja inicia com id INTEGER PRIMARY KEY UNIQUE
    '''
    if(not ver_existencia_tabela(que_banco, nome_da_tabela, quer_debug)):
        lista_aux = []
        string = ''
        for i in chaves:
            lista_aux.append(i)
        if (len(chaves) > 1):
            string = ','.join(lista_aux)
        else:
            string = chaves[0]
        sql = "CREATE TABLE "f'{nome_da_tabela}'"(id INTEGER PRIMARY KEY UNIQUE, "f'{string}'");"
        try:
            conexao = conexao_banco(que_banco)
            cursor = conexao.cursor()
            cursor.execute(sql)
            conexao.commit()
            if(quer_debug):
                print("Tabela "f'{nome_da_tabela}'" criada com sucesso!")
            return True
        except:
            if(quer_debug):
                print("Criação de tabela falhou!")
            return Error

#Metodos de consulta ===================================================================================================
def numero_colunas(que_save, qual_tabela):
    '''
        Consulta todas as linhas de uma tabela e captura a primeira;\n
        A primeria assim como qualquer outra é retornado como uma lista;\n
        Cada indice da lista é um item em uma coluna;\n
        Logo, o tamanho dessa lista é o tamanho de colunas da tabela;\n
        Retorna o numero de colunas da tabela <qual_tabela> no banco de dados <qual_save>;\n
    '''
    num_colunas = consultar_tabela(que_save, qual_tabela)
    if( num_colunas == []):
        return None
    else:
        return(len(num_colunas[0]))

def numero_linhas(que_save:str , qual_tabela: str, quer_debug=False):
    '''
        Retorna numero de linhas baseado no tamanho da lista que consultar() retorna
    '''
    tabela = consultar_tabela(que_save, qual_tabela, quer_debug)
    if(ver_existencia_tabela(que_save, qual_tabela)):
        if( tabela == []):
            if(quer_debug):
                print("Tabela "f'{qual_tabela}'" está vazia!")
            return None
        else:
            if (quer_debug):
                print("Tabela "f'{qual_tabela}'" possui "f'{len(tabela)}'" linhas!")
            return(len(tabela))
    else:
        if (quer_debug):
            print("Tabela "f'{qual_tabela}'" não existe!")
        return None

def consultar_coluna(que_save: str, qual_tabela: str, coluna_id: str, quer_debug=False):
    '''
    Retorna todas as colunas <qual_coluna> da tabel <qual_tabela>
    '''
    try:
        conexao = conexao_banco(que_save)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute("SELECT "f'{coluna_id}'" FROM "f'{qual_tabela}'";")
        resultado = cursor.fetchall()
        # Verificação da conexão via commit
        if(quer_debug):
            print('Consulta de coluna realizada com sucesso')
            print("Coluna "f'{coluna_id}'": "f'{resultado}'"")

        conexao.close()
        return resultado

    except:
        if(quer_debug):
            print('Consulta de coluna falhou!')
        return Error

def consultar_linha(que_banco: str, qual_tabela: str, chave_primaria: str, qual_linha: str, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Exige um inteiro <qual_linha> contendo o identificador da linha a ser retornada\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Retorna todas os colunas da linha <qual_linha>
    '''

    sql = "SELECT * FROM "f'{qual_tabela}'" WHERE "f'{chave_primaria}'"="f'{qual_linha}'";"
    try:
        conexao = conexao_banco(que_banco)
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        if(quer_debug):
            print('Consulta de linha realizada com sucesso:')
            print("Linha "f'{qual_linha}'": "f'{resultado}'"")
        conexao.close()
        return resultado

    except:
        if(quer_debug):
            print('Consulta de linha falhou!')
        return Error

def consultar_tabela(que_banco: str, qual_tabela: str, quer_debug=False):
    '''
    Retorna a tabela <qual_tabela> do banco de dados <qual_save>
    '''
    str = "SELECT * FROM "f'{qual_tabela}'";"
    try:
        conexao = conexao_banco(que_banco)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute(str)
        resultado = cursor.fetchall()
        # Verificação da conexão via commit
        if(quer_debug):
            print('Consulta de tabela realizada com sucesso')

        conexao.close()
        return resultado

    except:
        print('Consulta de tabela falhou!')

def consultar_linha_coluna(que_banco:str, qual_tabela: str,chave_primaria:str, qual_linha: str, qual_coluna: int, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Exige um inteiro <qual_linha> contendo o identificador da linha a ser verificado\n
    Exige um inteiro <qual_coluna> contendo o identificador da coluna a ser verificado\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Retorna o valor da coluna <qual_coluna>) na linha <qual_linha> da tabela <qual_tabela>
    '''

    linha = consultar_linha(que_banco,qual_tabela,chave_primaria,qual_linha, quer_debug)
    linha = linha [0]
    if (quer_debug):
        print("Consulta linha coluna realizada com sucesso!")
        print("Item na linha "f'{qual_linha}'" e coluna "f'{qual_coluna}'" da tabela "f'{qual_tabela}'":")
        print(linha[qual_coluna])
    return linha[qual_coluna]

def consultar_colunas(que_banco: str, qual_tabela: str, lista_colunas: list, quer_debug=False):
    '''
    Retorna os valores das linhas apenas das colunas <lista_colunas>\n
    '''
    # Chaves ===========================
    lista_aux = []
    for i in lista_colunas:
        lista_aux.append(i)
    if (len(lista_colunas) > 1):
        colunas = ','.join(lista_aux)
    else:
        colunas = lista_colunas[0]

    sql = "SELECT "f'{colunas}'" FROM "f'{qual_tabela}'";"
    try:
        conexao = conexao_banco(que_banco)
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        if (quer_debug):
            print('Consulta de colunaS realizada com sucesso')

        conexao.close()
        return resultado
    except:
        print('Consulta de colunaS falhou!')

def nome_das_colunas(que_save: str, qual_tabela: str, quer_debug=False):
    '''
    Retorna uma lista com os nomes das colunas da tabela <qual_tabela> do banco de dados <qual_save>
    '''
    try:
        conexao = conexao_banco(que_save)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        sql = "PRAGMA table_info("f'{qual_tabela}'");"
        cursor.execute(sql)
        tupla = cursor.fetchall()
        resultado = []
        for i in tupla:
            resultado.append(i[1])
        # Verificação da conexão via commit
        if(quer_debug):
            print('Consulta nome das colunas realizada com sucesso')
        conexao.close()
        return resultado
    except:
        if(quer_debug):
            print('Consultar nome das colunas falhou!')
        return None

def consulta_por_valor(que_save: str, qual_tabela: str, chave:str, valor: str, quer_debug = False):
    '''
    Retorna a linha com o valor <valor> na coluna <coluna>
    Retorna None em caso contrário
    '''
    todas_colunas = nome_das_colunas(save_teste, qual_tabela)
    # Chaves ===========================
    lista_aux = []
    for i in todas_colunas:
        lista_aux.append(i)
    if (len(todas_colunas) > 1):
        string1 = ','.join(lista_aux)
    else:
        string1 = todas_colunas[0]
    # Valores ===========================
    string2 = chave + " = "+ "\'" + valor + "\'"

    sql = "SELECT "f'{string1}'" FROM "f'{qual_tabela}'" WHERE "f'{string2}'"; "
    try:
        conexao = conexao_banco(que_save)
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        conexao.close()
        if(resultado == []):
            if (quer_debug):
                print("Nenhuma correspondencia encontrada para valor "f'{valor}'" na coluna "f'{chave}'"")
            return resultado

        if (quer_debug):
            print("A linha com valor "f'{valor}'" na coluna "f'{chave}'" é:")
            print(resultado)
        return resultado

    except:
        if (quer_debug):
            print('Consulta por valor falhou!')
        return None

#Metodos de manipulação ================================================================================================
def inserir(que_banco: str, qual_tabela: str, chaves: list, valores: list, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Exige uma lista de strings <chaves> contendo as chaves das colunas exceto o id primario\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Insere uma nova linha de valores na tabela <qual_tabela>
    '''
    #Chaves ===========================
    lista_aux = []
    for i in chaves:
        lista_aux.append(i)
    if (len(chaves) > 1):
        string2 = ','.join(lista_aux)
    else:
        string2 = chaves[0]
    #Valores ===========================
    lista_aux = []
    for i in valores:
        lista_aux.append("\'"+i+"\'")
    if(len(valores)>1):
        string3 = ','.join(lista_aux)
    else:
        string3 = "\'"+valores[0]+"\'"
    sql = "INSERT INTO "f'{qual_tabela}'" ("f'{string2}'") VALUES("f'{string3}'"); "
    try:
        conexao = conexao_banco(que_banco)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute(sql)
        # Verificação da conexão via commit
        conexao.commit()
        conexao.close()
        if(quer_debug):
            print("Inserido com sucesso.")
            print("Valores inseridos: "f'{string3}'" respectivamentes nas chaves: "f'{string2}'"")
    except:
        if(quer_debug):
            print('Inserir falhou!')
        return Error

def deletar_linha(que_save: str, qual_tabela: str, qual_linha: str):
    sql_delete = "DELETE FROM "f'{qual_tabela}'" WHERE id='"f'{qual_linha}'"' ;"
    try:
        conexao = conexao_banco(que_save)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute(sql_delete)
        # Verificação da conexão via commit
        conexao.commit()
        conexao.close()
        print("Linha "f'{qual_linha}'" da tabela "f'{qual_tabela}'" deletado com sucesso")
    except:
        print('Deletar falhou!')

def deletar_tabela(que_banco, qual_tabela, quer_debug=False):
    '''
       Exige uma string <que_banco> contendo o diretorio do banco de dados\n
       Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
       Um argumento opcional de debug, False por padrão:
           True caso você queria que o status da conexão seja impressa no console;\n
           False caso não;\n
       Deleta a tabela <qual_tabela> de <qual_banco>
    '''
    sql = "DROP TABLE "f'{qual_tabela}'";"
    try:
        conexao = conexao_banco(que_banco)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute(sql)
        # Verificação da conexão via commit
        conexao.commit()
        conexao.close()
        if (quer_debug):
            print("Tabela "f'{qual_tabela}'" deletado com sucesso")
    except:
        if (quer_debug):
            print('Deletar falhou!')
        return Error

def resetar_tabela(que_banco, qual_tabela, quer_debug=False):
    sql_delete = "DELETE FROM "f'{qual_tabela}'";"
    try:
        conexao = conexao_banco(que_banco)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute(sql_delete)
        # Verificação da conexão via commit
        conexao.commit()
        conexao.close()
        if(quer_debug):
            print("Tabela "f'{qual_tabela}'" foi resetada com sucesso")
    except:
        if(quer_debug):
            print('Resetar tabela falhou!')

def deletar_tabela_exceto(que_banco, qual_tabela_nao: list, quer_debug=False):
    '''
       Exige uma string <que_banco> contendo o diretorio do banco de dados\n
       Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
       Um argumento opcional de debug, False por padrão:
           True caso você queria que o status da conexão seja impressa no console;\n
           False caso não;\n
       Deleta a tabela <qual_tabela> de <qual_banco>
    '''
    string = ''
    lista_aux = []
    for i in qual_tabela_nao:
        lista_aux.append("\'" + i + "\'")
    if (len(qual_tabela_nao) > 1):
        string = ','.join(lista_aux)
    else:
        string = "\'" + qual_tabela_nao[0] + "\'"

    sql = "SELECT 'DROP TABLE ''' || name || ''';' FROM sqlite_master WHERE type = 'table' AND name NOT IN ("f'{string}'");"

    try:
        conexao = conexao_banco(que_banco)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute(sql)
        tupla = cursor.fetchall()
        for i in tupla:
            aux = i
            cursor.execute(aux[0])

        # Verificação da conexão via commit
        conexao.commit()
        conexao.close()
            # if(quer_debug):
            #     print("Tabela "f'{qual_tabela}'" deletado com sucesso")
    except:
        if (quer_debug):
            print('Deletar falhou!')
        return Error

def atualizar(que_banco: str, qual_tabela: str, qual_linha: str, chaves: list, valores: list, quer_debug=False):
    '''
         Exige uma string <que_banco> contendo o diretorio do banco de dados\n
         Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
         Exige um inteiro <qual_linha> contendo o identificador da linha a ser atualizada\n
         Um argumento opcional de debug, False por padrão:
             True caso você queria que o status da conexão seja impressa no console;\n
             False caso não;\n
    '''
    # Chaves ===========================
    lista_aux = []
    if(len(chaves) > 1):
        for i in range(len(chaves)):
            string_aux = chaves[i] + " = " +"\'" + valores[i] +"\'"
            lista_aux.append(string_aux)
        string1 = ', '.join(lista_aux)
    else:
        string1 = chaves[0] + " = " +"\'" + valores[0] +"\'"

    sql = "UPDATE "f'{qual_tabela}'" SET "f'{string1}'" WHERE id="f'{qual_linha}'" ;"
    try:
        conexao = conexao_banco(que_banco)
        # Objeto cursor pode executar funções sql
        cursor = conexao.cursor()
        cursor.execute(sql)
        # Verificação da conexão via commit
        conexao.commit()
        conexao.close()
        if(quer_debug):
            print("Valores atualizados: "f'{string1}'" respectivamentes nas chaves: "f'{chaves}'"")
        return True
    except:
        if(quer_debug):
            print('Atualizar falhou!')
        return False

def ver_existencia_tabela(que_banco: str, qual_tabela: str, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Um argumento opcional de debug, False por padrão:
         True caso você queria que o status da conexão seja impressa no console;\n
         False caso não;\n
    Verifica a existência da tabela <qual_tabela> no banco de dados <qual_save>
    '''

    try:
        conexao = conexao_banco(que_banco)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM  "f'{qual_tabela}'"")
        conexao.close()
        if(quer_debug):
            print("A tabela "f'{qual_tabela}'" JÁ existe no banco de dados "f'{que_banco}'" ")
        return True
    except sqlite3.OperationalError:
        if(quer_debug):
            print("A tabela "f'{qual_tabela}'" NÃO existe no banco de dados "f'{que_banco}'" ")
        return False

#Metodos AD-HOC  =======================================================================================================
def criar_tabela_save(que_banco: str, quantos_saves: int, quer_debug=False):
    '''
    Cria um save\n
    Exige uma string <que_banco> contendo o diretorio do banco de dados do save\n
    Exige uma string <nome_save> para nomear o save\n
    Cria uma tabela de nome <nome> com:
        - <quantos_saves>linhas contendo qual planta,o estado atual e os pontos atuais da planta no save atual\n
    Um argumento opcional de debug, False por padrão:
        -True caso você queria que o status da conexão seja impressa no console;\n
        -False caso não;\n
    '''
    if(not ver_existencia_tabela(que_banco, "save")):
        criar_tabela(que_banco, "save", ["planta","qual_estagio","pontos","dinheiro"], quer_debug)
        if(consultar_tabela(que_banco, "save") == []):
            for i in range(quantos_saves):
                inserir(que_banco,"save",["planta","qual_estagio","pontos","dinheiro"], ["Nenhuma","0","0","0"])
    else:
        ver_existencia_tabela(que_banco,  "save", quer_debug)

def get_planta_atual(que_banco: str, que_save: str, quer_debug = False):
    '''
        Retorna a planta presente no save <que_save>\n
    '''
    planta = consultar_linha_coluna(que_banco, 'save', "id", que_save, 1, quer_debug)
    return planta

def get_estagio_atual(que_banco: str, que_save: str, quer_debug = False):
    '''
        Retorna o numero do estagio atual da planta presente no save <que_save>\n
    '''
    estagio = consultar_linha_coluna(que_banco, 'save', "id", que_save, 2, quer_debug)
    return estagio

def set_planta_atual(que_banco: str, que_save: str, que_planta: str, quer_debug = False):
    '''
    Define a planta atual no save atual;\n
    Apenas plantas registradas na tabela de plantas podem ser setadas\n
    Retorna True caso seja setada com sucesso False em caso contrário
    '''
    #Verifica se a tabela de saves existe
    if(not ver_existencia_tabela(que_banco, "save")):
        if(quer_debug):
            print("A tabela de saves está indisponivel!")
        return False
    #Verifica se a tabela de plantas exsiste
    if(not ver_existencia_tabela(que_banco, "plantas")):
        if(quer_debug):
            print("A tabela de plantas está indisponivel!")
        return None
    #Se existir, uma lista de plantas verifica se a planta esta registrada
    aux = consulta_por_valor(que_banco,"plantas","nome",que_planta, quer_debug)
    if(aux == []):
        if (quer_debug):
            print("A planta "f'{que_planta}'" não está registrada!")
        return False
    #Caso a planta esteja registrada ela é setada no save atual
    planta = list(map(str,aux[0]))
    planta[2] = "1"
    del planta[0]
    if(atualizar(que_banco, "save", que_save, ["planta","qual_estagio","pontos"], planta, quer_debug)):
        if(quer_debug):
            print(""f'{que_planta}'" foi setado como a planta do save "f'{que_save}'"")
        return True
    else:
        if (quer_debug):
            print("Setar a planta no save falhou!")
        return False

def get_numero_estagios(que_banco: str, que_planta:str, quer_debug= False):
    '''
      Retorna o numero de estagios da planta <que_planta>
      '''
    if(ver_existencia_tabela(que_banco, "plantas")):
        plantas_e_estagios = consultar_colunas(que_banco,"plantas",["nome","estagios"],quer_debug)
        resultado = 'N/A'
        for i in plantas_e_estagios:
             if que_planta in i:
                 if(quer_debug):
                    print( i[1])
                 return i[1]

    else:
        print("Parece que não existe uma tabela de plantas válida!")
        return None

def ja_tem_algo_plantado(que_banco: str, que_save: str, quer_debug = False):
    o_que_ta_plantado = consultar_linha_coluna(que_banco, "save", "id", que_save, 1, quer_debug)
    if(o_que_ta_plantado != "Nenhuma"):
        if(quer_debug):
            print("A planta atual é: ", o_que_ta_plantado)
        return True
    else:
        if(quer_debug):
            print("Nada está plantado!")
        return False

def get_imagem_estagio_atual(que_banco: str, que_save: str, quer_debug = False):
    '''
        Retorna o nome do arquivo de imagem do estagio atual da planta presente no save <que_save>\n
        Se não houver nenhuma planta retona None
    '''
    #Verifica se tem algo
    if(ja_tem_algo_plantado(que_banco, que_save)):
        planta = get_planta_atual(que_banco, que_save)
        estagio = get_estagio_atual(que_banco, que_save)
        if (quer_debug):
            print(planta + "_" + estagio + ".png")

        return planta + "_" + estagio + ".png"
    else:
        if(quer_debug):
            print("Não tem nada plantado!")
        return None

def resetar_planta(que_banco: str, que_save: str, quer_debug = False):
    return atualizar(que_banco, "save", que_save, ["qual_estagio","pontos"], ["1","0"], quer_debug)

def resetar_save(que_banco: str, que_save: str, quer_debug = False):
    '''
    Reseta o save para o estado original
    '''
    # Verifica se a tabela de saves existe
    if (not ver_existencia_tabela(que_banco, "save")):
        if (quer_debug):
            print("A tabela de saves está indisponivel!")
        return False
    if (atualizar(que_banco, "save", que_save, ["planta", "qual_estagio", "pontos"],["Nenhuma","0","0"] , quer_debug)):
        if (quer_debug):
            print("Save "f'{que_save}'" foi resetado com sucesso!")
        return True
    else:
        if (quer_debug):
            print("Resetar o save "f'{que_save}'" falhou!")
        return False

def resetar_todos(que_banco: str, quer_debug = False):
    '''
    Reseta todos os saves para o estado original
    '''
    # Verifica se a tabela de saves existe
    if (not ver_existencia_tabela(que_banco, "save")):
        if (quer_debug):
            print("A tabela de saves está indisponivel!")
        return False
    #Verifica se ela esta vazia ou n
    qnt_saves = numero_linhas(que_banco,'save')
    if(qnt_saves == 0):
        if (quer_debug):
            print("A tabela de saves está vazia!")
        return False
    for i in range(qnt_saves):
        if (atualizar(que_banco, "save", f'{i}', ["planta", "qual_estagio", "pontos"],["Nenhuma","0","0"] , quer_debug)):
            if (quer_debug):
                print("Save "f'{i}'" foi resetado com sucesso!")
            if(i == qnt_saves):
                return True
        else:
            if (quer_debug):
                print("Resetar o save "f'{i}'" falhou!")
            return False

def atualizar_estagio(que_banco: str, que_save: str, quanto_de_incremento: int, quer_debug = False):
    '''
    Atualiza o estagio da planta atual sem ultrapassar o estagio max
    '''
    max_estagios  = int(get_numero_estagios(que_banco, get_planta_atual(que_banco, que_save)))
    estagio_atual = int(get_estagio_atual(save_teste, que_save))
    incremento = estagio_atual + quanto_de_incremento
    if( incremento > max_estagios):
        if(quer_debug):
            print("Impossivel atualizar, o incremento ultrapassa o limite!")
            print(""f'{max_estagios}'" é o limite max!")
            print(""f'{estagio_atual + quanto_de_incremento}'" é a tentativa de incremento!")
        return False

    if (atualizar(que_banco, "save", que_save, ["qual_estagio"], [f'{incremento}'], quer_debug)):
        if (quer_debug):
            print("O estagio da planta atual foi incrementado com sucesso!")
        return True
    else:
        if (quer_debug):
            print("Atualizar o estagio falhou!")
        return False

def registrar_produtos(que_banco: str, tipo_produto: str, valores, quer_debug = False):
    '''
    Registra produtos\n
       Produtos que já existem não são registrados\n
       Ponha <quer_debug> como true caso queira saber quais
    '''
    for i in valores:
        lista_aux = []
        lista_aux.append(i)
        colunas = nome_das_colunas(que_banco, tipo_produto)
        del colunas[0]
        for j in lista_aux:
            consulta = consulta_por_valor(que_banco, tipo_produto, "nome", j[0], quer_debug)
            if(consulta == None or consulta == []):
                inserir(que_banco, tipo_produto, colunas, j, quer_debug)
            else:
                if(quer_debug):
                    print("O seguite produto já esta registrado:")
                    print(consulta)

def get_produto(que_banco: str, tipo_produto: str, que_produto: str, quer_debug = False):
    '''Retorna uma lista com as informações sobre o produto <que_produto>'''
    produto = consulta_por_valor(que_banco, tipo_produto, "nome", que_produto ,quer_debug)
    if(produto == [] or produto == None):
        return None
    return produto

def get_imagem_produto(que_banco: str, tipo_produto: str, que_produto: str, quer_debug = False):
    '''Retorna o nome do arquivo de imagem do produto <que_produto>'''
    produto = get_produto(que_banco, tipo_produto, que_produto, quer_debug)
    if(produto == [] or produto == None):
        return None
    nome = produto[0][1]
    if(quer_debug):
        print(nome + ".png")
    return nome + ".png"

def get_icone_produto(que_banco: str, tipo_produto: str, que_produto: str, quer_debug = False):
    '''Retorna o nome do arquivo de imagem do produto <que_produto>'''
    produto = get_produto(que_banco, tipo_produto, que_produto, quer_debug)
    if(produto == [] or produto == None):
        return None
    nome = produto[0][1]
    if(quer_debug):
        print(nome + "_icone_off.png")
    return nome + "_icone_off.png"

def criar_tabela_inventarios(que_banco: str, quantos_espacos: int, quer_debug = False):
    '''Cria uma tabela do inventario caso não exista uma'''
    quantos_saves = numero_linhas(save_teste,"save",quer_debug)
    for i in range(1,quantos_saves+1):
        if(not ver_existencia_tabela(que_banco, f'inventario_{i}', quer_debug)):
            criar_tabela(save_teste, f'inventario_{i}', ["conteudo"], quer_debug)
            for j in range(quantos_espacos):
                inserir(que_banco,f'inventario_{i}',["conteudo"],["nada"])

def get_quantos_espacos(que_banco: str, que_inventario: int, quer_debug = False):
    '''Retorna a quantidade de espaços que o inventario possui'''
    if(ver_existencia_tabela(que_banco, f'inventario_{que_inventario}', quer_debug)):
        quantos_espacos = numero_linhas(que_banco, f'inventario_{que_inventario}', quer_debug)
        if(quer_debug):
            print("O inventario "f'inventario_{que_inventario}'" atualmente possui "f'{quantos_espacos}'" espaços!")
        return quantos_espacos

def get_quantos_espacos_vazios(que_banco: str, que_inventario: int, quer_debug = False):
    '''
    Retorna a quantidade de espaços vazios no inventario
    '''
    if(ver_existencia_tabela(que_banco,  f'inventario_{que_inventario}', quer_debug)):
        resultado = consulta_por_valor(que_banco, f'inventario_{que_inventario}',"conteudo", "nada", quer_debug)
        if(quer_debug):
            print("O inventario "f'inventario_{que_inventario}'" tem "f'{len(resultado)}'" espaços vazios!")
        return len(resultado)

def resetar_inventario(que_banco: str, que_inventario: int, quer_debug = False):
    '''
    Reseta o inventario para o estado de nada em todas as celulas
    '''
    if(ver_existencia_tabela(que_banco, f'inventario_{que_inventario}', quer_debug)):
        for i in range(get_quantos_espacos(que_banco, quer_debug)):
            atualizar(que_banco, f'inventario_{que_inventario}', f'{i}',["conteudo"],["nada"], quer_debug)

def get_inventario(que_banco: str, qual_inventario: int, quer_debug = False):
    '''
    Retorna uma lista com o conteudo do inventario
    '''
    if(ver_existencia_tabela(que_banco, f'inventario_{qual_inventario}', quer_debug)):
        resultado = consultar_tabela(que_banco, f'inventario_{qual_inventario}', quer_debug)
        if(quer_debug):
            print("O inventario está no seguinte estado:")
            for i in resultado:
                print(f'Slot:{i[0]} | {i[1]}')
        return resultado

def alterar_espaco(que_banco: str, que_inventario: int, que_espaco:str, por_o_que: str, quer_debug = False):
    '''
    Atualiza o espaço <que_espaço> com o valor <por_o_que>
    '''
    if(ver_existencia_tabela(que_banco, f'inventario_{que_inventario}', quer_debug)):
        atualizar(que_banco, f'inventario_{que_inventario}', que_espaco, ["conteudo"], [por_o_que], quer_debug)

def get_save_atual(que_banco: str, quer_debug = False):
    return consultar_linha_coluna(que_banco,"save_atual","id",'1',1,quer_debug)

def set_save_atual(que_banco: str, novo_atual: str, quer_debug = False):
    return atualizar(que_banco,"save_atual",'1',["que_save"],[novo_atual],quer_debug)

def gerar_carrinho(que_banco: str, inventario:str, quer_debug = False):
    for i in inventario:
        inserir(que_banco, 'carrinho', ['produto'], [i[1]], quer_debug)

def get_carrinho(que_banco: str, quer_debug=False):
    '''
    Retorna uma lista com o conteudo do carrinho
    '''
    if(ver_existencia_tabela(que_banco, 'carrinho', quer_debug)):
        resultado = consultar_tabela(que_banco, 'carrinho', quer_debug)
        if(quer_debug):
            print("O carrinho está no seguinte estado:")
            for i in resultado:
                print(f'Slot:{i[0]} | {i[1]}')
        return resultado

def set_carrinho(que_banco: str, o_que: str ,quer_debug=False):
    carro = get_carrinho(que_banco, quer_debug)
    for i in range (len(carro)):
        if(carro[i][1] == 'nada'):
            slot = (carro[i][0])
            atualizar(que_banco, "carrinho", slot, ["produto"], [f'{o_que}'], quer_debug)
            return slot
    return "cheio"

resetar_tabela(save_teste, "carrinho", True)
def get_saldo(que_banco: str, que_save: str, quer_debug=False):
    saldo = consultar_linha_coluna(que_banco,'save','id', que_save, 4, quer_debug)
    return saldo

def sacar(que_banco: str, que_save: str, valor_de_saque: int, quer_debug=False):
    saldo = int(get_saldo(que_banco, que_save, quer_debug))
    if(saldo - valor_de_saque < 0):
        return 1
    atualizar(que_banco,'save',que_save,['dinheiro'],[saldo - valor_de_saque < 0])
    return 2

def depositar(que_banco: str, que_save: str, valor_de_saque: int, quer_debug=False):
    saldo = int(get_saldo(que_banco, que_save, quer_debug))
    if(saldo + valor_de_saque < 0):
        return 1
    atualizar(que_banco,'save',que_save,['dinheiro'],[saldo + valor_de_saque < 0])
    return 2

#Teste =================================================================================================================
#print(get_numero_estagios(produtos, "feijao_mandragora"))
#get_estagio_atual(save_teste)
#atualizar_estagio(save_teste,1,True)
#deletar_tabela(save_teste,"tomate")
#get_nome_tabela_save(save_teste, True)
#inserir_estagios("tomate", 5, "200")
#printconsultar_linha("tomate", 3, "../banco_de_dados/save.db"))
#criar_tabela_save(save_teste)
#get_estagio_atual("../banco_de_dados/save.db")#
#inserir("../banco_de_dados/save.db", ['planta'], ["tomate"])
#print(numero_linhas(save_teste, "tomate"))
#atualizar(save_teste,"save_1",["planta", "qual_estagio","pontos"],["cereja","0","300"])
#atualizar(save_teste, "save_1", 1, ["planta","qual_estagio","pontos"],["tomate","1","200"])
#get_estagio_atual(save_teste, "save_1")
#consultar_linha_coluna(save_teste,"save_1",1,"qual_estagio")
#deletar_planta(save_teste, 'tomate', True)#
# consulta_por_valor(save_teste, "plantas", "nome", "tomate", True)
# consulta_por_valor(save_teste, "plantas", "nome", "feijao_mandragora", True)
# set_planta_atual(save_teste, 1, "feijao_mandragora")
# get_estagio_atual(save_teste, '1', True)

# lista = []
# lista.append(["pá_de_cobre","1", "200"])
# lista.append(["pá_de_ferro","2", "400"])
# lista.append(["pá_de_prata","3", "800"])
# lista.append(["pá_de_ouro" ,"2", "1600"])
# criar_tabela(save_teste,"plantas",["nome","estagios","pontos","preco"])
# deletar_tabela(save_teste,"plantas", True)
# criar_tabela(save_teste,"plantas",["nome","estagios","pontos","preco"])
# lista = []
# lista.append(["regador_de_ouro","4", "100"])

# registrar_produtos(save_teste, "ferramentas", lista, True)
# deletar_tabela(save_teste,"save",True)
# criar_tabela_save(save_teste,3,True)
# criar_tabela_inventario_temp(save_teste, 6,True)
# criar_tabela_save_temp(save_teste)
# resetar_inventario(save_teste)
# get_inventario(save_teste, True)
# alterar_espaco(save_teste, "5", "pá_de_ferro",True)
# get_icone_produto(save_teste, "plantas", "tomate",True)
# alterar_espaco(save_teste, 3,3,"regador_de_prata",True)
# resetar_save(save_teste,'1')
# criar_tabela(save_teste,"save_atual",["que_save"])
# inserir(save_teste,"save_atual",["que_save"],["1"])
# deletar_tabela(save_teste,"inventario_1", True)
# deletar_tabela(save_teste,"inventario_2", True)
# deletar_tabela(save_teste,"inventario_3", True)
# criar_tabela_inventarios(save_teste, 6, True)
# criar_tabela(save_teste, 'carrinho', ['produto'],True)