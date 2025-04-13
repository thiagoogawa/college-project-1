import mysql.connector

#faz conexao inicial com o banco
def conecta_banco():

    conexao = mysql.connector.connect (
        host = 'localhost',
        port=3307,
        user = 'root',
        password = '123456',
        database = 'Projeto_Integrador_II',
    )

    cursor = conexao.cursor()
    return cursor, conexao


def executa_POST(command): # conseguiu criar => 'sucesso'
    cursor, conexao = conecta_banco()

    cursor.execute(command)
    conexao.commit()
    cursor.close()
    conexao.close()
    return "sucesso" 


def executa_GET(command): # conseguiu pegar => elemento do banco
    cursor, conexao = conecta_banco()

    cursor.execute(command)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()
    return resultado


def executa_GET_BY_ID(command): # conseguiu pegar => elemento do banco
    cursor, conexao = conecta_banco()

    cursor.execute(command)
    resultado = cursor.fetchone()[0]

    cursor.close()
    conexao.close()
    return resultado


def executa_PUT(command): # conseguiu alterar => 'sucesso'
    cursor, conexao = conecta_banco()

    cursor.execute(command)
    conexao.commit()
    
    cursor.close()
    conexao.close()

    return "sucesso"


def executa_DELETE(command): # conseguiu deletar => 'sucesso'
    cursor, conexao = conecta_banco()

    cursor.execute(command)
    conexao.commit()
    cursor.close()
    conexao.close()
    return "sucesso"

########## FUNÇÃO PRINCIPAL (CHAMA AS FUNÇÕES ESPECIFICAS) ##########

def executar_comando(method, command):
                    
    match method:
        case "POST":
            return executa_POST(command)
        
        case "GET":
            return executa_GET(command)
        
        case "GET_BY_ID":
            return executa_GET_BY_ID(command)
        
        case "PUT":
            return executa_PUT(command)
        
        case "DELETE":
            return  executa_DELETE(command)
        case _:
            return "MÉTODO INVÁLIDO"
    return " "


    