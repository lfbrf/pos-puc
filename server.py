####################################################################################
# TITULO do arquivo python: server.py
# AUTOR:
# Data: 04/02/2023 | PERIODO: 2023.2  | Versão: 0.2
# OBJETIVO DESSE ARQUIVO: Criar o web service com flask e aplicar a CRUD.
####################################################################################


# Importar as bibliotecas
# Flask - web service | render_template e redirect - indexação html | request - requisiçoes web
from flask import Flask, render_template, request, redirect
import funcoes as fun  # importa o modulo com as funções
import sqlite3 # manipulação do banco de dados


app = Flask(__name__)                                           # definir o app
database_filename = "database.db"                               # define o arquio de banco de dados
app.config["SECRET_KEY"] = "hahaa ardse tfcyg uhygf ijhuy"      # define a senha de configuração



valid = False                   # variavel de verificação de usuario logado | Se logado > True | se deslogado > False
login = []                      # login[0] = email| login[1] = password | login[2] = userId
eventoIdUpdate = []             # eventoId
olds = []
cont = 0
# função de escrever dados no banco de dados - passando o comand sql como parametro
def db_write(sql, data=None):
    connection = sqlite3.connect(database_filename)     # cria a conexão
    connection.row_factory = sqlite3.Row                # usa o metodo row do sqlite3
    db = connection.cursor()                            # cria ocursor que usaremos para manipular o banco
    if data:
        rows_affected = db.execute(sql, data).rowcount  # conta se houver alterações no banco
    else:
        rows_affected = db.execute(sql).rowcount        # não escreve
    connection.commit()                                 # comando commit para salvar alterações
    db.close()                                          # fecha o banco
    connection.close()                                  # fecha a conexão
    return rows_affected                                # retorna a quantidade de linhas alteradas

# função de ler dados no banco de dados - passando o comand sql como parametro
def db_read(sql, data=None):
    connection = sqlite3.connect(database_filename)          # cria a conexão
    connection.row_factory = sqlite3.Row                     # usa o metodo row do sqlite3
    db = connection.cursor()                                 # cria ocursor que usaremos para manipular o banco
    if data:
        db.execute(sql, data)                                # executa ocomando sql com o parametro
    else:
        db.execute(sql)                                      # executa ocomando sql com o parametro
    leitura = db.fetchall()                                  # coleta todos os resultados do comando
    rows = [dict(dado) for dado in leitura]                  # transforma em dicionário para manipularmos os dados
    db.close()                                               # fecha o banco
    connection.close()                                       # fecha a conexão
    return rows                                              # retorna a dicionário


#pagina inicial- ok
@app.route("/")                                 # define o caminho/link/url
def index_page():                               # cria a função desse caminho
    global valid
    if valid == False:
        return redirect("/login_page")              # redireciona para o caminho de login
    else:
        return redirect("/main_page")


#pagina de registro de usuarios - ok
@app.route("/registro_page",  methods=["POST", "GET"])      # define o caminho/link/url e o metodo
def registro_page():                                        # cria a função desse caminho
    global valid
    if valid == False:
        msg = "Bem vindo"
        try:
            form = dict(request.values)                             # coleta os dados do formulario html dessa pagina
            msg = "Bem vindo"

            # testa se o formulario voltou vazio ou preenchido (> 0)
            if len(form) > 0:
                # coleta os dados do formulario e aloca nas variaveis
                email = form["userid"]
                nome = form["nome"]
                password=form["password"]

                # testa as variaveis se são validas
                if fun.validar_nome(nome) == 1 and fun.email_certo(email) == 1 and len(fun.validar_campo(email, "usuario", "email")) == 0 and len(password) > 0:
                    # escreve no banco de dados e envia a mensagem de gravado com sucesso
                    db_write("INSERT into usuario (nome, email, password) VALUES('%s', '%s', '%s');" % (nome, email,password))
                    msg="Usuario Criado com Sucesso"
                # caso os dados sejam invalidos, não grava nada e volta a mensagem de dados invalidos
                else:
                    msg="Dados Inválidos"
            return render_template("user_cadastro.html", msg=msg)  # renderiza a pagina de cadastro de usuario

        except:
            return render_template("user_cadastro.html", msg=msg)  # renderiza a pagina de cadastro de usuario
    else:
        return redirect("/login_page")


#pagina de login - ok
@app.route("/login_page", methods=["GET"])   # define o caminho/link/url e o metodo GET - (via link)
def login_page():                            # cria a função desse caminho
    global valid
    if valid == False and cont == 0:
        return render_template("login.html")     # renderiza a pagina de login
    else:
        return redirect("/main_page")


@app.route("/login_page", methods=["POST"]) # define o caminho/link/url e o metodo POST - (via botão)
def login_request():                        # cria a função desse caminho
    global valid, cont
    if valid == False and cont < 1:
        global login                            # indica que a variável 'login' se trata da varialvel global
        form = dict(request.values)             # coleta os dados do formulario html dessa pagina

        # le o banco de dados e busca pelos usuarios com o email e senha insformados no formulario
        users = db_read("SELECT * FROM usuario WHERE email='%s' AND password= '%s'" % (form["userid"], form["password"]))
        email = form["userid"]
        login=[email, form["password"]]

        # se houver resposta [email e senha iguais ao informados]
        if len(users) == 1:
            valid = True                        # define a variavel global para TRUE > usuario logado com email e senha corretos
            cont += 1
            return redirect("/main_page")       # renderiza a pagina do usuario

        # se não houver resposta [email e senha não correspondem]
        else:
            return redirect("/login_page")      # renderiza a pagina de login
    else:
        return redirect("/main_page")


#pagina de logout - ok
@app.route("/logout_page")                  # define o caminho/link/url
def logout_page():                          # cria a função desse caminho
    global valid, cont                      # indica que a variável 'login' se trata da varialvel global
    valid = False                           # define a variavel global para FALSE > usuario deslogado
    cont = 0
    return redirect("/login_page")    # renderiza a pagina de login


#pagina principal
@app.route("/main_page", methods=["GET"])                           # define o caminho/link/url e o metodo - GET
def main_page():                                                    # cria a função desse caminho
    global valid
    if valid == True:                                               # testa se usuário esta logado
        user = db_read("SELECT * FROM usuario ORDER BY userId;")    # coleta os dados dos usuarios
        id=0                                                        # define o ID como 0
        nm = ""                                                     # define o nome como ''
        for d in user:                                              # testa para cada usuario
            if d["email"] == login[0] and d["password"]==login[1]:  # se o login e a senha são iguais aos informados
                id=d["userId"]      # define o ID como o userId
                nm=d["nome"]        # define o nome do usuario
            else:
                pass
        itens = db_read("SELECT * FROM eventos WHERE userId='%i';" % id)  # coleta os itens do usuario de ID encontrado
        return render_template("main.html", nome=nm, itens=itens)         # renderiza a pagina inicial do usuario
    else:                                                           # se não estiver logado
        return redirect("/login_page")                              # redirecio para a pagina de login


#pagina principal
@app.route("/main_page", methods=["post"])                          # define o caminho/link/url e o metodo - GET
def main_request():                                                 # cria a função desse caminho
    global valid
    if valid == True:                                               # testa se usuário esta logado
        user = db_read("SELECT * FROM usuario WHERE email = '%s'" % login[0])       # coleta os dados pelo email
        itens = db_read("SELECT * FROM eventos ORDER BY nome;")                     # coleta os dados pelo nome
        return render_template("main.html", nome="Usuario", itens=itens)            # renderiza a pagina inicial do usuario
    else:                                                                           # se não estiver logado
        return redirect("/login_page")                                              # redirecio para a pagina de login


#pagina de registro de evento - ok | CREATE OK
@app.route("/main_page_novo_evento",  methods=["POST", "GET"])  # define o caminho/link/url e o metodo
def main_page_create():                                         # cria a função desse caminho
    global valid
    if valid == True:
        try:   # testa se metodo é POST - via botão
            nome = request.form['taskname']             # aceita qualquer valor - se vazio será cadastrado como 'empty'
            descricao = request.form['taskdescription'] # aceita qualquer valor - se vazio será cadastrado como 'empty'
            data = request.form['taskdate']             # aceita apenas datas no ano de 2023 - agenda de 2023

            hora = request.form['taskhour']             # valores entre 00:00 a 23:59
            endereco = request.form['tasklocal']        # aceita qualquer valor - se vazio será cadastrado como 'empty'
            dado = fun.data_to_write(login, nome, descricao, data, hora, endereco)  # retorna uma lista com dados
            if dado[2] != "Empty":
                temp = dado[2].split("-")
                dado[2] = (temp[2]+'-'+temp[1]+'-'+temp[0])


            # escreve os dados na tabela eventos
            db_write("INSERT into eventos (nome, descricao, dia, hora, endereco, userId) "
                     "VALUES('%s', '%s', '%s','%s', '%s', '%s');" % (dado[0], dado[1],dado[2],dado[3],dado[4],dado[5]))
            return redirect("/main_page")               # redireciona para a pagina do usuario
        except:
            return redirect("/main_page")  # redireciona para a pagina do usuario
    else:
        return redirect("/login_page")



# pagina de consulta de evento - ok | READ OK
@app.route("/main_page_consultar", methods=["POST"])            # define o caminho/link/url e o metodo
def main_page_read():                                                  # cria a função desse caminho
    global valid
    if valid == True:              # testa se metodo é POST - via botão
        try: # trata metodo get
            user = db_read("SELECT userId FROM usuario WHERE email = '%s';" % login[0])           # coleta o userId
            id = user[0]["userId"]
            form = dict(request.values)                                                          # recebe o eventoId
            evento = db_read("SELECT * FROM eventos WHERE eventoId = '%i';" % int(form['see']))   # coleta dados do evento
            eNome = evento[0]['nome']
            eDescricao = evento[0]['descricao']
            eDia = evento[0]['dia']
            eHora = evento[0]['hora']
            eEndereco = evento[0]['endereco']

            # renderiza a pagina de consulta
            return render_template("read.html", nome=eNome, dia=eDia, hora=eHora, descricao=eDescricao, endereco=eEndereco)
        except:
            return redirect("/main_page")

    else:                                       # caso não esteja logado
        return redirect("/login_page")          # direciona para a pagina de login

# pagina de atualização de evento - ok | UPDATE OK
@app.route("/main_page_atualizar",  methods=["POST"])                # define o caminho/link/url e o metodo
def main_page_update():                                              # cria a função desse caminho
    global valid, olds
    global eventoIdUpdate                                            # define que será usado a variavel global
    if valid == True:  # testa se metodo é POST - via botão
        try:  # trata metodo get
            user = db_read("SELECT userId FROM usuario WHERE email = '%s';" % login[0])
            id = user[0]["userId"]
            form = dict(request.values)
            evento = db_read("SELECT * FROM eventos WHERE eventoId = '%i';" % int(form['refresh']))
            eventoIdUpdate = int(form['refresh'])
            eNome = evento[0]['nome']
            eDescricao = evento[0]['descricao']
            eDia = evento[0]['dia']
            eHora = evento[0]['hora']
            eEndereco = evento[0]['endereco']
            olds = [eNome, eDescricao, eDia, eHora, eEndereco]
            print(olds)
            return render_template("update.html", nome=eNome, dia=eDia, hora=eHora, descricao=eDescricao, endereco=eEndereco)
        except:
            return redirect("/main_page")

    else:  # caso não esteja logado
        return redirect("/login_page")  # direciona para a pagina de login


# pagina de atualização de evento - ok | UPDATE OK
@app.route("/main_page_atualizar_dados",  methods=["POST"])   # define o caminho/link/url e o metodo
def main_page_update_dados():                                 # cria a função desse caminho
    global eventoIdUpdate, valid, olds                        # define que será usado a variavel global
    if valid == True:                                         # testa se o usuário está logado
        try:    # trata metodo get
            newname = request.form["newname"]               # Novo nome
            newdia = request.form["newdia"]                 # Novo dia - data
            newhora = request.form["newhora"]               # Nova hora
            newdescricao = request.form["newdescricao"]     # Nova descrição
            newendereco = request.form["newendereco"]       # Novo endereço
            dado = fun.data_to_write(login, newname, newdescricao, newdia, newhora, newendereco)  # retorna uma lista com dados
            news = [dado[0], dado[1], dado[2], dado[3], dado[4]]
            dados = fun.compare_dados(olds, news)

            # reescreve os dados na tabela eventos
            db_write("UPDATE eventos SET nome='%s', descricao='%s', dia='%s', hora='%s', endereco='%s' WHERE eventoId='%i';"
                     % (dados[0], dados[1], dados[2], dados[3], dados[4], int(eventoIdUpdate)))
            return redirect("/main_page")  # redireciona para a pagina do usuario
        except:
            return redirect("/main_page")
    else:  # caso não esteja logado
        return redirect("/login_page")  # direciona para a pagina de login


@app.route("/main_page_deletar", methods=["POST", "GET"])      # define o caminho/link/url e o metodo
def main_page_deletar():                                       # cria a função desse caminho
    global valid
    global eventoIdUpdate  # define que será usado a variavel global
    if valid == True:      # testa se metodo é POST - via botão
        try:  # trata metodo get
            user = db_read("SELECT userId FROM usuario WHERE email = '%s';" % login[0])
            id = user[0]["userId"]
            form = dict(request.values)
            print(id, form['remove'])

            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("delete from eventos where eventoId = '%i';" % int(form['remove']))  # deleta os eventos do usuario
            con.commit()  # executa e salva as alterações no banco
            return redirect("/main_page")
        except:
            return redirect("/main_page")
    else:
        return redirect("/login_page") # direciona para a pagina de login


# deleta todos os eventos - limpa a lista de eventos do usuario - OK
@app.route("/main_page_deletar_eventos", methods=["POST", "GET"])              # define o caminho/link/url e o metodo
def main_page_deletar_eventos():   # cria a função desse caminho
    global valid
    if valid == True:              # testa se usuario está logado
        try:                       # trata metodo get
            user = db_read("SELECT userId FROM usuario WHERE email = '%s';" % login[0])  # coleta o userId
            id = user[0]["userId"]
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("delete from eventos where userId = '%s'" % int(id)) # deleta os eventos do usuario
            con.commit()                                                     # executa e salva as alterações no banco
            return redirect("/main_page")
        except:
            return redirect("/main_page")
    else:                                       # caso não esteja logado
        return redirect("/login_page")          # direciona para a pagina de login



# deleta a conta  - OK
@app.route("/main_page_deletar_user", methods=["POST", "GET"])              # define o caminho/link/url e o metodo
def main_page_deletar_user():   # cria a função desse caminho
    global valid
    if valid == True:              # testa se usuario está logado
        try:                       # trata metodo get
            user = db_read("SELECT userId FROM usuario WHERE email = '%s';" % login[0])  # coleta o userId
            id = user[0]["userId"]
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("delete from eventos where userId = '%s'" % int(id)) # deleta os eventos do usuario
            cur.execute("delete from usuario where userId = '%s'" % int(id))  # deleta o usuario
            con.commit()                                                     # executa e salva as alterações no banco
            return redirect("/login_page")
        except:
            return redirect("/main_page")
    else:                                       # caso não esteja logado
        return redirect("/login_page")          # direciona para a pagina de login



if __name__ =="__main__":
    app.run(host="0.0.0.0", port=80, debug=True)