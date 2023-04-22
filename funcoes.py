import sqlite3
import server as s

# CRUD - CRIAR | CONSULTAR | ATUALIZAR | DELETAR
conexao_bd = None

def iniciar():
    global conexao_bd
    conexao_bd = sqlite3.connect("database.db")

def listar_tabela(tabela): # função usada para listar a tabela escolhida
    iniciar()
    conex_c = conexao_bd.cursor()
    conex_sel = conex_c.execute("SELECT * FROM %s" % tabela)
    conexao_bd.commit()
    resp = conex_sel.fetchall()
    conex_c.close()
    return resp


def validar_campo(campo_teste, tabela, campo_tabela):
    iniciar()
    conex_c = conexao_bd.cursor()
    conex_sel = conex_c.execute("SELECT * FROM %s WHERE %s = '%s'" % (tabela, campo_tabela, campo_teste))
    conexao_bd.commit()
    resp = conex_sel.fetchall()
    conex_c.close()
    return resp

def test_string(variavel):
    cont = 0
    try:
        variavel = int(variavel)
        cont += 0
    except:
        cont += 10
    return cont

def validar_nome(nome_teste):
    contador = 0
    nome = nome_teste.split(' ')
    lista = []
    for i in nome:
        if i != ' ' and i != '':
            lista.append(i)
    textual = test_string(nome_teste)
    if len(lista) > 1 and textual > 0:
        contador += 1
    else:
        contador += 0
    return contador

def email_certo (email):
    contador = 0
    lista = email.split("@")
    l = lista[0]
    if test_string(email) > 0 and len(lista) == 2 and len(lista[0]) >= 1 and len(lista[1]) > 5 and len(
            email.split(" ")) == 1:
        if len(l.split(".com")) == 1 or len(l.split(".com.br")) == 1:
            l2 = lista[1]
            if len(l2.split(".com")) == 2 or len(l2.split(".com.br")) == 2:
                contador += 1
            else:
                pass
        else:
            pass
    else:
        pass
    return contador

def endereco_certo(endereco):
    existe = (validar_campo(endereco, 'eventos', 'endereco'))
    cont = 0
    if len(existe) == 1:
        if endereco == existe[0][2]:
            cont += 10
        else:
            cont-=10
        cont += 5
    return cont

def listar_eventos(id):
    dicionario = s.db_read("SELECT * FROM eventos WHERE userId='%i';" % id)
    for item in dicionario:
        print(item)

def caracter(nome):
    retorno = "Empty"
    letras = (nome.count("")-1) - nome.count(" ") # caracteres
    if len(nome) > 0 and letras > 0:
        # a pessa digitou algo
        retorno = nome
    else:# não foi digitado nada ou apenas espaços
        pass
    return retorno

def data_to_write(login, nome, descricao, data, hora, local):
    user = s.db_read("SELECT * FROM usuario ORDER BY userId;")

    id = 0
    for d in user:
        if d["email"] == login[0] and d["password"] == login[1]:
            id = d["userId"]
        else:
            pass
    dt = ""

    if caracter(data) == "Empty":
        dt = caracter(data)
    else:
        temp = caracter(data).split("-")
        dt = str(temp[2]+'-'+temp[1]+'-'+temp[0])


    dados = [caracter(nome), caracter(descricao), dt, caracter(hora), caracter(local), id]
    return dados


def compare_dados(olds, news):
    dado = []
    for i in range(len(olds)):
        print(olds[i], "|", news[i])
        if news[i] == "Empty":
            dado.append(olds[i])
        else:
            dado.append(news[i])
    return dado