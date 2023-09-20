import sqlite3
from sqlite3 import Error

#Metodo de coZnexão =====================================================================================================
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
    Exige uma string <nome_da_tabela> para nomear a tabela\n
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
def numero_colunas(que_banco, qual_tabela):
    '''
        Consulta todas as linhas de uma tabela e captura a primeira;\n
        A primeria assim como qualquer outra é retornado como uma lista;\n
        Cada indice da lista é um item em uma coluna;\n
        Logo, o tamanho dessa lista é o tamanho de colunas da tabela;\n
        Retorna o numero de colunas da tabela <qual_tabela> no banco de dados <que_banco>;\n
    '''
    num_colunas = consultar_tabela(que_banco, qual_tabela)
    if( num_colunas == []):
        return None
    else:
        return(len(num_colunas[0]))

def numero_linhas(que_banco:str, qual_tabela: str, quer_debug=False):
    '''
        Retorna numero de linhas baseado no tamanho da lista que consultar() retorna
    '''
    tabela = consultar_tabela(que_banco, qual_tabela, quer_debug)
    if(ver_existencia_tabela(que_banco, qual_tabela)):
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

def consultar_coluna(que_banco: str, qual_tabela: str, coluna_id: str, quer_debug=False):
    '''
    Retorna todas as colunas <qual_coluna> da tabel <qual_tabela>
    '''
    try:
        conexao = conexao_banco(que_banco)
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
    Retorna a tabela <qual_tabela> do banco de dados <que_banco>
    '''
    str = "SELECT * FROM "f'{qual_tabela}'";"
    # try:
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

    # except:
    #     print('Consulta de tabela falhou!')

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

def nome_das_colunas(que_banco: str, qual_tabela: str, quer_debug=False):
    '''
    Retorna uma lista com os nomes das colunas da tabela <qual_tabela> do banco de dados <que_banco>
    '''
    try:
        conexao = conexao_banco(que_banco)
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

def consulta_por_valor(que_banco: str, qual_tabela: str, chave:str, valor: str, quer_debug = False):
    '''
    Retorna a linha com o valor <valor> na coluna <coluna>
    Retorna None em caso contrário
    '''
    todas_colunas = nome_das_colunas(que_banco, qual_tabela)
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
        conexao = conexao_banco(que_banco)
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

def deletar_linha(que_banco: str, qual_tabela: str, qual_linha: str):
    sql_delete = "DELETE FROM "f'{qual_tabela}'" WHERE id='"f'{qual_linha}'"' ;"
    try:
        conexao = conexao_banco(que_banco)
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

