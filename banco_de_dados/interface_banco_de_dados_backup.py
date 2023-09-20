import sqlite3
from sqlite3 import Error

#Metodo de conexão =====================================================================================================
def conexao_banco(que_banco: str, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Conecta a um banco de dados\n
    Retorna a conexão caso seja bem sucedido\n
    Retorna Error caso contrário
    '''
    quer_debug = quer_debug
    if(quer_debug):
        try:
            conexao = None
            conexao = sqlite3.connect(que_banco)
            print('Conectado')
            return conexao
        except:
            print('Conexão broxou')
            return Error
    else:
        try:
            conexao = None
            conexao = sqlite3.connect(que_banco)
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
    quer_debug = quer_debug
    if (quer_debug):
        if(not ver_existencia(que_banco, nome_da_tabela)):
            lista_aux = []
            string = ''
            for i in chaves:
                lista_aux.append(i)
            if (len(chaves) > 1):
                string = ','.join(lista_aux)
            else:
                string = chaves[0]
            print(string)
            sql = "CREATE TABLE "f'{nome_da_tabela}'"(id INTEGER PRIMARY KEY UNIQUE, "f'{string}'");"
            try:
                conexao = conexao_banco(que_banco)
                cursor = conexao.cursor()
                cursor.execute(sql)
                conexao.commit()
                print("Tabela "f'{nome_da_tabela}'" criada com sucesso!")
                return True
            except:
                print("Criaçãoo de tabela falhou!")
                return Error
        else:
            print("Essa tabela já existe!")
    else:
        if (not ver_existencia(que_banco, nome_da_tabela)):
            lista_aux = []
            string = ''
            for i in chaves:
                lista_aux.append(i)
            if (len(chaves) > 1):
                string = ','.join(lista_aux)
            else:
                string = chaves[0]
            print(string)
            sql = "CREATE TABLE "f'{nome_da_tabela}'"(id INTEGER PRIMARY KEY UNIQUE, "f'{string}'");"
            try:
                conexao = conexao_banco(que_banco)
                cursor = conexao.cursor()
                cursor.execute(sql)
                conexao.commit()
                return True
            except:
                return Error
        else:
            print("Essa tabela já existe!")

#Metodos de consulta ===================================================================================================
def numero_colunas(que_banco: str, qual_tabela: str, quer_debug=False):
    '''
        Exige uma string <que_banco> contendo o diretorio do banco de dados\n
        Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
        Um argumento opcional de debug, False por padrão:
            True caso você queria que o status da conexão seja impressa no console;\n
            False caso não;\n
        Retorna o numero de colunas da tabela <qual_tabela> no banco de dados <que_banco>;\n
        Retorna None caso a tabela esteja vazia;
    '''
    quer_debug = quer_debug
    if (quer_debug):
        num_colunas = consultar_tabela(que_banco, qual_tabela)
        if( num_colunas == []):
            print("A tabela "f'{qual_tabela}'" está vazia!")
            return None
        else:
            print("A tabela "f'{qual_tabela}'" tem "f'{len(num_colunas[0])}'" colunas")
            return(len(num_colunas[0]))
    else:
        num_colunas = consultar_tabela(que_banco, qual_tabela)
        if (num_colunas == []):
            return None
        else:
            return (len(num_colunas[0]))

def numero_linhas(que_banco, qual_tabela, quer_debug=False):
    '''
        Exige uma string <que_banco> contendo o diretorio do banco de dados\n
        Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
        Um argumento opcional de debug, False por padrão:
            True caso você queria que o status da conexão seja impressa no console;\n
            False caso não;\n
        Retorna o número de linhas da tabela;
        Retorna None caso esteja vazia
    '''
    quer_debug = quer_debug
    if (quer_debug):
        num_colunas = consultar_tabela(que_banco, qual_tabela)
        if (num_colunas == []):
            print("A tabela "f'{qual_tabela}'" está vazia!")
            return None
        else:
            print("A tabela "f'{qual_tabela}'" tem "f'{len(num_colunas)}'" linhas")
            return (len(num_colunas))
    else:
        num_colunas = consultar_tabela(que_banco, qual_tabela)
        if (num_colunas == []):
            return None
        else:
            return (len(num_colunas))

def consultar_coluna(que_banco: str, qual_tabela: str, coluna_id: str, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Exige uma string <coluna_id> contendo o identificador da coluna a ser verificado\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Retorna todas os valores na coluna <coluna_id> da tabela <qual_tabela>
    '''
    quer_debug = quer_debug
    if (quer_debug):
        try:
            sql = "SELECT "f'{coluna_id}'" FROM "f'{qual_tabela}'";"
            conexao = conexao_banco(que_banco)
            cursor = conexao.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
            print('Consulta realizada com sucesso:')
            print("Itens da coluna "f'{coluna_id}'":")
            print(resultado)
            conexao.close()
            return resultado

        except:
            print('Consultar falhou!')
            return Error
    else:
        try:
            sql = "SELECT "f'{coluna_id}'" FROM "f'{qual_tabela}'";"
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
            # Verificação da conexão via commit
            conexao.close()
            return resultado

        except:
            return Error

def consultar_linha(que_banco: str, qual_tabela: str, qual_linha: int, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Exige um inteiro <qual_linha> contendo o identificador da linha a ser retornada\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Retorna todas os colunas da linha <qual_linha>
    '''

    quer_debug = quer_debug
    if (quer_debug):
        sql = "SELECT * FROM "f'{qual_tabela}'" WHERE id="f'{qual_linha}'";"
        try:
            conexao = conexao_banco(que_banco)
            cursor = conexao.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
            print('Consulta realizada com sucesso:')
            print("Colunas da linha "f'{qual_linha}'": "f'{resultado}'"")
            conexao.close()
            return resultado

        except:
            print('Consultar falhou!')
            return Error
    else:
        sql = "SELECT * FROM "f'{qual_tabela}'" WHERE id="f'{qual_linha}'";"
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
            # Verificação da conexão via commit
            conexao.close()
            return resultado

        except:
            return Error

def consultar_tabela(que_banco: str, qual_tabela: str, quer_debug=False):
    '''
    Retorna a tabela <qual_tabela> do banco de dados <que_banco>\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    '''
    try:
        sql = "SELECT * FROM "f'{qual_tabela}'";"
        conexao = conexao_banco(que_banco)
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        if(quer_debug):
            print('Consulta realizada com sucesso:')
            for i in resultado:
                print(i)
        conexao.close()
        return resultado

    except:
        if(quer_debug):
            print('Consultar falhou!')
        return Error

def consultar_linha_coluna(que_banco:str, qual_tabela: str, qual_linha: int, qual_coluna: int, quer_debug=False):
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
    if(quer_debug):
        linha = consultar_linha(que_banco,qual_tabela, qual_linha)
        linha = linha [0]
        print("Item na linha "f'{qual_linha}'" e coluna "f'{qual_coluna}'" da tabela "f'{qual_tabela}'":")
        print(linha[qual_coluna])
        return linha[qual_coluna]
    else:
        linha = consultar_linha(que_banco, qual_tabela, qual_linha)
        linha = linha[0]
        return linha[qual_coluna]

def nome_das_colunas(que_banco: str, qual_tabela: str, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Um argumento opcional de debug, False por padrão:
        True caso você queria que o status da conexão seja impressa no console;\n
        False caso não;\n
    Retorna uma lista com os nomes das colunas da tabela <qual_tabela> do banco de dados <qual_save>
    '''
    if(quer_debug):
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
            print(""f'{qual_tabela}'" tem as seguintes colunas:")
            print(resultado)
            conexao.close()
            return resultado
        except:
            print('Consultar falhou!')
    else:
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
            conexao.close()
            return resultado
        except:
            return Error

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
    if(quer_debug):
        sql = "INSERT INTO "f'{qual_tabela}'" ("f'{string2}'") VALUES("f'{string3}'"); "
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql)
            # Verificação da conexão via commit
            conexao.commit()
            conexao.close()
            print("Inserido com sucesso.")
            print("Valores inseridos: "f'{string3}'" respectivamentes nas chaves: "f'{string2}'"")
        except:
            print('Inserir falhou!')
            return Error
    else:
        sql = "INSERT INTO "f'{qual_tabela}'" ("f'{string2}'") VALUES("f'{string3}'"); "
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql)
            # Verificação da conexão via commit
            conexao.commit()
            conexao.close()
        except:
            return Error

def deletar_linha(que_banco: str, qual_tabela: str, qual_linha: str, quer_debug=False):
    '''
     Exige uma string <que_banco> contendo o diretorio do banco de dados\n
     Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
     Exige um inteiro <qual_linha> contendo o identificador da linha a ser apagada\n
     Um argumento opcional de debug, False por padrão:
         True caso você queria que o status da conexão seja impressa no console;\n
         False caso não;\n
     Delete a linha <qual_linha> na tabela <qual_tabela>
     '''
    if(quer_debug):
        sql_delete = "DELETE FROM "f'{qual_tabela}'" WHERE id='"f'{qual_linha}'"' ;"
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql_delete)
            # Verificação da conexão via commit
            conexao.commit()
            conexao.close()
        except:
            return Error
    else:
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
            return Error

def deletar_tabela(que_banco, qual_tabela, quer_debug=False):
    '''
       Exige uma string <que_banco> contendo o diretorio do banco de dados\n
       Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
       Um argumento opcional de debug, False por padrão:
           True caso você queria que o status da conexão seja impressa no console;\n
           False caso não;\n
       Deleta a tabela <qual_tabela> de <qual_banco>
    '''
    if(quer_debug):
        sql_delete = "DROP TABLE "f'{qual_tabela}'";"
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql_delete)
            # Verificação da conexão via commit
            conexao.commit()
            conexao.close()
            print("Tabela "f'{qual_tabela}'" deletado com sucesso")
        except:
            print('Deletar falhou!')
            return Error
    else:
        sql_delete = "DROP TABLE "f'{qual_tabela}'";"
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql_delete)
            # Verificação da conexão via commit
            conexao.commit()
            conexao.close()
        except:
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

    if(quer_debug):
        sql = "UPDATE "f'{qual_tabela}'" SET "f'{string1}'" WHERE id="f'{qual_linha}'" ;"
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql)
            # Verificação da conexão via commit
            conexao.commit()
            conexao.close()
            print("Valores atualizados: "f'{string1}'" respectivamentes nas chaves: "f'{chaves}'"")
        except:
            print('Atualizar falhou!')
            return Error
    else:
        sql = "UPDATE "f'{qual_tabela}'" SET "f'{string1}'" WHERE id="f'{qual_linha}'" ;"
        try:
            conexao = conexao_banco(que_banco)
            # Objeto cursor pode executar funções sql
            cursor = conexao.cursor()
            cursor.execute(sql)
            # Verificação da conexão via commit
            conexao.commit()
            conexao.close()
        except:
            print('Atualizar falhou!')
            return Error

def ver_existencia(que_banco: str, qual_tabela: str, quer_debug=False):
    '''
    Exige uma string <que_banco> contendo o diretorio do banco de dados\n
    Exige uma string <qual_tabela> contendo o identificador da tabela a ser verificada\n
    Um argumento opcional de debug, False por padrão:
         True caso você queria que o status da conexão seja impressa no console;\n
         False caso não;\n
    Verifica a existência da tabela <qual_tabela> no banco de dados <qual_save>
    '''
    if(quer_debug):
        try:
            conexao = conexao_banco(que_banco)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM  "f'{qual_tabela}'"")
            conexao.commit()
            conexao.close()
            print("A tabela "f'{qual_tabela}'" existe no banco de dados "f'{que_banco}'" ")
            return True

        except sqlite3.OperationalError:
            print("A tabela "f'{qual_tabela}'" NÃO existe no banco de dados "f'{que_banco}'" ")
            return False
    else:
        try:
            conexao = conexao_banco(que_banco)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM  "f'{qual_tabela}'"")
            conexao.commit()
            conexao.close()
            return True

        except sqlite3.OperationalError:
            return False

#Testes ================================================================================================================
# banco_teste = "../banco_de_dados/banco_teste.db"
# print("Teste1 ----------------------------------")
# conexao_banco(banco_teste, False)                      #Passagem por referencia ou
# conexao_banco("../banco_de_dados/banco_teste.db", True)#Direto
#
# print("\nTeste2 ----------------------------------")
# criar_tabela(banco_teste,"teste_1",["cliente VARCHAR(60) NOT NULL, salario INTEGER NOT NULL"],True)
# criar_tabela(banco_teste,"teste_2",["cliente VARCHAR(60) NOT NULL, salario INTEGER NOT NULL"],True)
#
# print("\nTeste3 ----------------------------------")
# numero_colunas(banco_teste,"teste_1",True)
#
# print("\nTeste4 ----------------------------------")
# numero_linhas(banco_teste,"teste_1",True)
#
# print("\nTeste5 ----------------------------------")
# consultar_coluna(banco_teste, "teste_1", "id", True)
# consultar_coluna(banco_teste, "teste_1", "cliente", True)
# consultar_coluna(banco_teste, "teste_1", "salario", True)
#
# print("\nTeste6 ----------------------------------")
# consultar_linha(banco_teste, "teste_1", 1, True)
# consultar_linha(banco_teste, "teste_1", 2, True)
# consultar_linha(banco_teste, "teste_1", 3, True)
#
# print("\nTeste7 ----------------------------------")
# consultar_tabela(banco_teste, "teste_1", True)
#
# print("\nTeste8 ----------------------------------")
# consultar_linha_coluna(banco_teste, "teste_1", 1, 1, True)
#
# print("\nTeste8 ----------------------------------")
# nome_das_colunas(banco_teste,"teste_1", True)
#
# print("\nTeste9 ----------------------------------")
# #inserir(banco_teste,"teste_1",['cliente','salario'], ["Lucas","500"], True)
#
# print("\nTeste10 ----------------------------------")
# #deletar_linha(banco_teste, "teste_1", 2)
#
# print("\nTeste11 ----------------------------------")
# deletar_tabela(banco_teste,"teste_2")
#
# print("\nTeste12 ----------------------------------")
# atualizar( banco_teste, "teste_1", 6,["cliente","salario"],["Ciro","30"], True)


lista = consultar_tabela( "../banco_de_dados/save.db", "tomate")
print("#1 ======================================================")
print(lista)
print("\n#2 ======================================================")
print(lista[0])
print("\n#3 ======================================================")
print(lista[0][1])