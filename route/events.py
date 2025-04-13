from flask import Blueprint, request, jsonify, render_template
from database.database import executar_comando
from datetime import date
import smtplib
from email.message import EmailMessage
from decimal import Decimal
from datetime import datetime

event_routes = Blueprint('events', __name__)



################################## Funções auxiliares ##################################



#função que verifica se o usuário é um admin ou não checando um array onde registramos os admins manualmente.
#depois que registrar o admin pelo banco de dados, manualmente, colocar o id que foi gerado para ele aqui dentro do array (list of admins).
def is_admin(user_id):
    list_of_admins = ['1','2'] #Primeiras contas criadas no banco são os admins.

    if user_id in list_of_admins:
        return True
    else:
        return False

#função que verifica se o usuário existe no banco pelo ID (e se existe, está autenticado)
def is_authenticated(user_id):
    
    comando = f'SELECT EXISTS(SELECT 1 FROM usuarios WHERE user_id = {user_id})'

    #Retorna se existe usuário no banco com as características enviadas
    retorno = executar_comando("GET", comando)

    if retorno == [(1,)]:
        return True
    else:
        return False

#ENVIAR E-GMAIL COM GMAIL:
def enviar_email(email, motivo):
    corpo_email = f'''
    <h1>[PROJETO INTEGRADOR 2]:</h1><br>
    <hr>
    <b>Seu evento foi reprovado pelo Administrador da plataforma!<b/><br>
    
    <h3>Motivo: {motivo}<h3/> 
    <hr>
    <i>Projeto Integrador 2 - PUC Campinas<i/>
    '''

    msg = EmailMessage()
    msg['Subject'] = "Evento Negado! - PI 2"
    msg['From'] = 'estudos.flask@gmail.com'
    msg['To'] = email
    msg['X-Priority'] = '1'
    
    password = 'oxixdpspqzdfiuip'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    #Login com as credenciais:
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print(f'Email enviado para {email}')

    return 'sucesso'



################################## Rotas de eventos - PARTE 1 ##################################



@event_routes.route('/', methods=['GET']) # retorna todos os eventos
def events():

    #pega user_id do header da requisição recebida
    user_id = request.headers.get('id')

    #verifica se o usuário está autenticado (True ou False)
    if is_authenticated(user_id):

        #lógica de selecionar todos eventos do banco
        comando = f'SELECT * FROM eventos'

        #retorna todos os eventos selecionados => elemento do banco
        retorno = executar_comando("GET", comando)

        if retorno:
            return jsonify(retorno), 200 # todos eventos
        else:
            return {"Status": 'erro ao selecionar todos eventos do banco de dados'}, 400

    else:
        return {"Status": f'Usuário ID:[{user_id}] não autenticado!'}, 400 # usuário não autenticado

@event_routes.route('/new', methods=['POST'])
def add_new_event():
    
    #pega user_id do header da requisição recebida
    user_id = request.headers.get('id')

    #verifica se o usuário está autenticado (True ou False)
    if is_authenticated(user_id):

        # pega dados do evento enviados na requisição
        data = request.json

        title = data.get('title') # maximo 50 caracteres
        descricao = data.get('descricao') # maximo 150 caracteres
        valor_de_cada_cota = data.get('valor_de_cada_cota') # minimo 1,00

        # validacoes do valor (minimo 1,00)
        if valor_de_cada_cota < 1.00: return {"Status": 'O valor de cota deve ser superior a R$ 1,00'}, 400

        periodo_para_apostar_inicio = data.get('periodo_para_apostar_inicio') # data + hora
        periodo_para_apostar_fim = data.get('periodo_para_apostar_fim') # data + hora
        data_acontecimento = data.get('data_acontecimento') #dia-mes-ano

        # forma query
        comando = f'INSERT INTO eventos (user_id_criador, title, descricao, valor_de_cada_cota, periodo_para_apostar_inicio, periodo_para_apostar_fim, data_acontecimento) VALUES ("{user_id}", "{title}", "{descricao}", {valor_de_cada_cota}, "{periodo_para_apostar_inicio}", "{periodo_para_apostar_fim}", "{data_acontecimento}")'

        # retorna sucesso se conseguiu adicionar o evento no banco
        retorno = executar_comando("POST", comando)

        if retorno == "sucesso":
            return {"Status": f'O evento [{title}] foi criado'}, 200 # evento criado
        else:
            return {"Status": 'erro ao criar evento no banco de dados'}, 400 # erro

    else:
        return {"Status": f'Usuário ID:[{user_id}] não autenticado!'}, 400

@event_routes.route('/searchEventByParam', methods=['POST'])
def get_events():

    user_id = request.headers.get('id')

    if is_authenticated(user_id):

        data = request.json

        parametro_de_busca = data.get('parametro_de_busca').upper()

        match parametro_de_busca:
            case "PENDENTE": #OK

                #pegar todos eventos que o usuario é dono e que está status pendente.
                comando = f'SELECT * FROM eventos WHERE status_de_publicacao = "pendente" AND user_id_criador = {user_id}'

                retorno = executar_comando("GET", comando)

                return jsonify(retorno), 200 # retornar todos eventos pendentes

            case "FINALIZADOS": #OK
                data_atual = datetime.now().replace(microsecond=0)
                data_atual = datetime.now().strftime("%Y-%m-%d")

                comando = f'SELECT * FROM eventos WHERE periodo_para_apostar_fim < "{data_atual}" AND status_de_publicacao = "aprovado"'

                retorno = executar_comando("GET", comando)

                return jsonify(retorno), 200 # retornar todos eventos finalizados

            case "FUTUROS":
                data_atual = datetime.now().replace(microsecond=0)
                data_atual = datetime.now().strftime("%Y-%m-%d")

                comando = f'SELECT * FROM eventos WHERE periodo_para_apostar_fim > "{data_atual}" AND status_de_publicacao = "aprovado"'

                return executar_comando("GET", comando)
            
            case _:
                return {'Erro': 'Parâmetro incorreto'}

    else:
        return {'Erro': 'Usuário não autenticado'}

@event_routes.route('/<int:event_id>/delete', methods=['POST'])
def delete_event_by_id(event_id):
    
    user_id = request.headers.get('id')

    if is_authenticated(user_id):

        comando = f'SELECT EXISTS(SELECT * FROM apostas WHERE event_id = {event_id})'
        retorno_aposta = executar_comando("GET", comando)
        
        comando = f'SELECT status_de_publicacao FROM Eventos WHERE event_id = {event_id}'
        retorno_status = executar_comando("GET", comando)

        if retorno_aposta == [(0,)] and retorno_status != 'aprovado':
            
            # deleta o evento
            comando = f'UPDATE Eventos SET is_ativo = 0 WHERE event_id = {event_id}'
            retorno = executar_comando("PUT", comando)

            if retorno == 'sucesso':
                return {'Sucesso': f'O evento {event_id} foi deletado com sucesso!'}
            else:
                return {'Erro': 'Erro ao deletar evento'}
        else:
            return {'Erro': 'Erro ao deletar evento'}    
        
    else:
        return {'Erro': 'Usuário não autenticado'}

#Esta rota o admin usa para avaliar se o evento que o usuario cadastrou pode ser publicado ou não
@event_routes.route('/<int:event_id>/evaluateNewEvent', methods=['PUT'])
def eval_event(event_id):
    admin_id = request.headers.get('id')

    if is_admin(admin_id):

        data = request.json

        is_ativo_bool = data.get('bool')
        novo_status = data.get('status').lower()
        
        status_possiveis = ['texto confuso', 'texto inapropriado', 'não respeita a política de privacidade e/ou termos de uso da plataforma', 'pendente', 'aprovado']
        
        if (novo_status in status_possiveis) and (is_ativo_bool == 0 or is_ativo_bool == 1):

            comando = f'UPDATE Eventos SET is_ativo = {is_ativo_bool}, status_de_publicacao = "{novo_status}" WHERE event_id = {event_id}'
            retorno_alteracao = executar_comando("PUT", comando)

            if retorno_alteracao == 'sucesso':
                if novo_status == 'aprovado':
                    return {"Sucesso": f'O status do evento [{event_id}] foi alterado para ["{novo_status}"]!'}, 200
                
                else:    
                    #ENVIAR EMAIL PARA O DONO DO EVENTO AVISANDO QUE O EVENTO FOI REPROVADO!

                    #Pegando o [ID] do usuário dono do evento passado no parâmetro
                    comando = f'SELECT user_id_criador FROM eventos WHERE event_id = {event_id}'
                    user_id_criador = executar_comando("GET_BY_ID", comando)
                    
                    #Pegando o [EMAIL] do usuário dono do evento passado no parâmetro
                    comando = f'SELECT email FROM usuarios WHERE user_id = {user_id_criador}'
                    email_criador_do_evento = executar_comando("GET_BY_ID", comando)
                    
                    enviar_email(email_criador_do_evento, novo_status)
                    
                    return {"Sucesso": f'Evento [{event_id}] reprovado!\nStatus alterado para: ["{novo_status}"]\nE-mail enviado para ["{email_criador_do_evento}"]'}, 200
                
        else:
            return {f'Erro': f'Favor enviar parâmetros corretos'}, 404
    else:
        return {'Erro': 'Usuario precisa ser admin!'}, 404



################################## Rotas de eventos - PARTE 2 (APOSTA) ##################################
############################# (após o evento ter sido cadastrado e aprovado) ############################



@event_routes.route('/<int:event_id>/betOnEvent', methods=['PUT'])
def bet_on_event(event_id):

    user_id = request.headers.get('id')

    if is_authenticated(user_id):

        data = request.json

        #Obter informações da requisição
        opcao_apostada_sim_ou_nao = data.get('opcao') #'sim' ou 'não'
        qtd_cotas_apostadas = data.get('cotas')
        
        #Validar se evento existe e está aprovado (apto para receber apostas)
        comando = f'SELECT EXISTS(SELECT * FROM Eventos WHERE event_id = {event_id} AND status_de_publicacao = "aprovado")'
        retorno = executar_comando("GET_BY_ID", comando)

        if retorno <= 0: return {"Erro": 'Evento inexistente.'}, 400

        #Obter titulo do evento
        comando = f'SELECT title FROM Eventos WHERE event_id = {event_id}'
        event_title = executar_comando("GET_BY_ID", comando)

        #Verifica quanto ele precisa para apostar (qtd de cotas apostadas * valor de cada cota para este evento)
        comando = f'SELECT valor_de_cada_cota FROM Eventos WHERE event_id = {event_id}'
        valor_de_cada_cota = executar_comando("GET_BY_ID", comando)

        valor_necessario = valor_de_cada_cota * qtd_cotas_apostadas

        #Obter saldo do usuário
        comando = f'SELECT saldo FROM Carteira WHERE user_id_dono = {user_id}'
        saldo = executar_comando("GET_BY_ID", comando)

        #Validar se possui saldo
        if saldo < valor_necessario:
            return {'Erro': 'Saldo insuficiente para criar aposta!'}, 400

        else:
            #Criar aposta
            comando = f'INSERT INTO Apostas (user_id_apostador, event_id, opcao_apostada_sim_ou_nao, qtd_cotas_apostadas) VALUES ("{user_id}", "{event_id}", "{opcao_apostada_sim_ou_nao}", {qtd_cotas_apostadas})'
            executar_comando("POST", comando)

            #Calcula saldo atualizado para o usuário apostador
            saldo_atualizado = saldo - valor_necessario

            #Debita o valor da conta do usuário
            comando = f'UPDATE Carteira SET saldo = {saldo_atualizado} WHERE user_id_dono = {user_id}'
            executar_comando("PUT", comando)

            #Adiciona na lista de valores gastos com apostas na carteira deste usuário
            comando = f'''
            UPDATE Carteira 
            SET historico_creditos_apostados = JSON_ARRAY_APPEND(historico_creditos_apostados, '$', JSON_OBJECT('Aposta realizada', {valor_necessario}))
            WHERE user_id_dono = {user_id}
            '''
            
            retorno = executar_comando("PUT", comando)
            
            if retorno == 'sucesso':
                return {'Sucesso': f'Você realizou uma aposta no evento {event_id} - {event_title}'}, 200
            else:
                return {'Erro': f'Problema ao apostar no evento {event_id}'}, 400
    else:
        return {'Erro': 'Usuário não autenticado'}, 400

#Esta rota o admin usa para dar o veredito se o evento ocorreu ou não, premiando os vencedores proporcionalmente
@event_routes.route('/<int:event_id>/finishEvent', methods=['PUT']) 
def finish_event(event_id):
    
    user_id = request.headers.get('id')
    
    if is_admin(user_id):
        
        data = request.json

        veredito = data.get('veredito') # sim ou não

        #Verificando se evento existe
        comando = f'SELECT EXISTS(SELECT 1 FROM Eventos WHERE event_id = {event_id})'
        retorno = executar_comando("GET_BY_ID", comando)

        if retorno < 1: #evento não existe
            return {'Erro': 'Evento inexistente'}
        
        #verificando se houveram apostas nele
        comando = f'SELECT EXISTS(SELECT 1 FROM Apostas WHERE event_id = {event_id})' 
        retorno = executar_comando("GET_BY_ID", comando)

        if retorno < 1: #não existem apostas neste evento

            #FINALIZAR EVENTO (ALTERAR is_ativo = 0) 
            comando = f'UPDATE Eventos SET is_ativo = 0 WHERE event_id = {event_id}'
            retorno = executar_comando("PUT", comando)

            return {'Sucesso': 'Evento encerrado.'}
        
        #Lógica para premiar os vencedores!

        #Obtem total de cotas dos vencedores
        comando = f"SELECT SUM(qtd_cotas_apostadas) FROM Apostas WHERE event_id = {event_id} AND opcao_apostada_sim_ou_nao = '{veredito}'"
        total_cotas_vencedores = executar_comando("GET_BY_ID", comando)

        #Obtem total de cotas dos perdedores
        comando = f"SELECT SUM(qtd_cotas_apostadas) FROM Apostas WHERE event_id = {event_id} AND opcao_apostada_sim_ou_nao <> '{veredito}'"
        total_cotas_perdedores = executar_comando("GET_BY_ID", comando)
        
        if total_cotas_perdedores == None: # Se ele vier None, é porque não houveram perdedores.
            total_cotas_perdedores = 0

        #Obtem IDs dos vencedores (apenas 1 vez, pois eles podem ter apostado mais vezes)
        comando = f"SELECT user_id_apostador FROM Apostas WHERE event_id = {event_id} AND opcao_apostada_sim_ou_nao = '{veredito}' LIMIT 1"
        lista_usuarios_vencedores = executar_comando("GET", comando)
        
        if len(lista_usuarios_vencedores) == 0:
            comando = f'UPDATE Eventos SET is_ativo = 0 WHERE event_id = {event_id}'
            retorno = executar_comando("PUT", comando)

            return {'Sucesso': 'Ninguém ganhou a aposta - Evento finalizado!'}, 200
        
        for user_id in lista_usuarios_vencedores:
            
            #Obtem quantidade de cotas apostadas pelo vencedor (somadas)
            comando = f"SELECT SUM(qtd_cotas_apostadas) FROM Apostas WHERE user_id_apostador = {user_id[0]} AND event_id = {event_id}"
            qtd_cotas_vencedor = executar_comando("GET_BY_ID", comando) 
            
            #Obtem valor de cada cota para este evento
            comando = f'SELECT valor_de_cada_cota FROM Eventos WHERE event_id = {event_id}'
            valor_de_cada_cota = executar_comando("GET_BY_ID", comando)
            
            premiacao = (Decimal(qtd_cotas_vencedor / total_cotas_vencedores) * Decimal(total_cotas_perdedores)) * (valor_de_cada_cota)
            
            if premiacao == 0:
                comando = f'UPDATE Eventos SET is_ativo = 0 WHERE event_id = {event_id}'
                retorno = executar_comando("PUT", comando)
                return {'Status': 'Todos ganharam a aposta e não obtiveram lucro - Evento Finalizado!'}, 200

            #Obtem saldo atual do usuario
            comando = f'SELECT Saldo FROM Carteira WHERE user_id_dono = {user_id[0]}'
            saldo_atual = executar_comando("GET_BY_ID", comando)

            #Premiando o usuário ganhador
            novo_saldo = Decimal(saldo_atual) + Decimal(premiacao)

            comando = f'UPDATE Carteira SET Saldo = {novo_saldo} WHERE user_id_dono = {user_id[0]}'
            retorno = executar_comando("PUT", comando)

        comando = f'UPDATE Eventos SET is_ativo = 0 WHERE event_id = {event_id}'
        retorno = executar_comando("PUT", comando)
        
        return {'Sucesso': 'Evento encerrado.'}, 200
        
    else:
        return {'Erro': 'Usuário não autenticado (Apenas administradores podem realizar esta tarefa).'}

@event_routes.route('/searchEvent', methods=['GET'])
def search_event():
    
    user_id = request.headers.get('id')

    if is_authenticated(user_id):

        #Captura palavra enviada na requisição
        #data = request.json
        #palavra_de_busca = data.get('palavra')
        palavra_de_busca = request.args.get('palavra') 
        #Faz busca no banco de dados
        comando = f"SELECT * FROM Eventos WHERE descricao LIKE '%{palavra_de_busca}%'"
        retorno = executar_comando("GET", comando)
        
        if len(retorno) == 0: #Se estiver vazio
            return {'Sucesso': 'Não há eventos com esta palavra-chave em sua descrição'}, 400
        else:
            return {f'Eventos com a palavra-chave {palavra_de_busca}': f'{retorno}'}, 200

    else:
        return {'Erro': 'Usuário não autenticado'}, 400


@event_routes.route('/criarEventos', methods=['GET'])
def exibe_form_criar_eventos():
    return render_template('criar_eventos.html')

@event_routes.route('/meusEventos', methods=['GET'])
def exibe_form_meus_eventos():
    return render_template('meus_eventos.html')

@event_routes.route('/historicoMeusEventos', methods=['GET'])
def historico_meus_eventos():
    user_id = request.headers.get('id')

    comando = f'SELECT event_id,title, status_de_publicacao FROM eventos WHERE user_id_criador = {user_id} AND is_ativo = 1'
    resultado = executar_comando("GET", comando)

    if len(resultado) == 0:
        return {"Status": 'Nenhum evento encontrado'}, 200

    return jsonify(resultado)


@event_routes.route('/apostarEvents', methods=['GET'])
def exibe_form_apostar_eventos():
    return render_template('apostar.html')

@event_routes.route('/retornaEventos', methods=['GET'])
def retorna_todos_os_eventos():
    user_id = request.headers.get('id')

    if is_authenticated(user_id):
        
        comando = f"""
            SELECT event_id, title, descricao, valor_de_cada_cota, 
            periodo_para_apostar_inicio, periodo_para_apostar_fim, data_acontecimento 
            FROM eventos WHERE status_de_publicacao = 'aprovado' AND is_ativo = 1
        """

        retorno = executar_comando("GET", comando)

        return jsonify(retorno) 
    else:
        return jsonify({'Erro': 'Usuário não autenticado'}), 401


@event_routes.route('/formbuscarEventos', methods=['GET'])
def exibe_form_buscar_eventos():
    return render_template('buscar_eventos.html')


@event_routes.route('/vencendo', methods=['GET'])
def retorna_eventos_proximo_vencimento():
    user_id = request.headers.get('id')

    if is_authenticated(user_id):

        comando = f"""
                    SELECT * 
                    FROM eventos 
                    WHERE periodo_para_apostar_fim BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
                    ORDER BY periodo_para_apostar_fim ASC
                    LIMIT 3;
                """
        
        resultado = executar_comando('GET', comando)

        return jsonify(resultado) 
    else:
        return jsonify({'Erro': 'Usuário não autenticado'}), 401
    

@event_routes.route('/maisApostados', methods=['GET'])
def retorna_eventos_mais_apostados():

    user_id = request.headers.get('id')

    if is_authenticated(user_id):

        comando = f"""SELECT 
                a.event_id, 
                e.title AS nome_evento, 
                SUM(a.qtd_cotas_apostadas) AS total_apostas
            FROM 
                apostas AS a
            JOIN 
                eventos AS e 
            ON 
                a.event_id = e.event_id
            GROUP BY 
                a.event_id, e.title
            ORDER BY 
                total_apostas DESC
            LIMIT 3;
        """   
        
        resultado = executar_comando('GET', comando)

        print(resultado)

        return jsonify(resultado) 
    else:
        return jsonify({'Erro': 'Usuário não autenticado'}), 401
    


    