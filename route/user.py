from flask import Blueprint, render_template, request, url_for, jsonify, redirect
from database.database import executar_comando
from route.events import is_authenticated
from decimal import Decimal


user_routes = Blueprint('users', __name__)

# Serviço para o CADASTRO do usuário na plataforma
@user_routes.route('/signUp', methods=['POST']) # receber em JSON pq nao eh "visivel"
def register_user():
    data = request.json

    nome = data.get('nome')
    cpf = data.get('cpf')
    data_nascimento = data.get('data_nascimento')
    email = data.get('email')
    senha = data.get('senha')

    comando = f'SELECT EXISTS(SELECT * FROM usuarios WHERE email = "{email}")'
    retorno = executar_comando("GET_BY_ID", comando)

    if retorno > 0:
        return {"Erro": 'Já existe um usuário com este e-mail.'}, 500
    
    else:        
        #INSERINDO usuario no banco
        comando = f'INSERT INTO usuarios (nome, cpf, data_nascimento, email, senha ) VALUES("{nome}", "{cpf}", "{data_nascimento}", "{email}", "{senha}")'
        retorno = executar_comando("POST", comando)
        
        #pegando ID do usuario que acaba de ser criado
        comando = f'SELECT user_id FROM usuarios WHERE email = "{email}" AND senha = "{senha}" LIMIT 1'
        user_id = executar_comando("GET_BY_ID", comando)

        #CRIAR CARTEIRA inicial zerada para o usuário
        comando = f'''
        INSERT INTO Carteira (
            user_id_dono, saldo, historico_compras_creditos, historico_creditos_apostados, data_ultimo_saque, valor_acumulado_saques_diarios
        ) VALUES (
            {user_id}, 0, JSON_ARRAY(), JSON_ARRAY(), "2024-10-10", 0
        );
    '''
        
        #return resposta de sucesso na criação da carteira inicial
        retorno = executar_comando("POST", comando)

        if retorno == 'sucesso':
            return {"Status": 'sucesso'}, 201 # padronizar retornos em JSON - tudo que nao é visivel será via JSON (req e res)
        else:
            return {"Status": 'erro'}, 500

# Serviço para exibir o formulário de LOGIN na plataforma
@user_routes.route('/loginForm', methods=['GET'])
def exibe_form_login():
    return render_template('login.html')

# Serviço para exibir o formulário de CADASTRO na plataforma
@user_routes.route('/signUpForm', methods=['GET'])
def exibe_form_cadastro():
    return render_template('cadastrar_usuario.html')

# Serviço para exibir o formulário de addFunds na plataforma
@user_routes.route('/addFundsForm', methods=['GET'])
def exibe_form_addFunds():
    return render_template('addFunds.html')

@user_routes.route('/minhaWalletForm', methods=['GET'])
def exibe_form_minhaWallet():
    return render_template('minha_wallet.html')

@user_routes.route('/withdrawForm', methods=['GET'])
def exibe_form_withdrawFunds():
    return render_template('withdraw_Funds.html')

# Serviço para executar o LOGIN na plataforma
@user_routes.route('/login', methods=['POST'])
def login_user():

    data = request.json

    email = data.get('email')
    senha = data.get('senha')
    
    comando = f'SELECT * FROM usuarios WHERE email = "{email}" AND senha = "{senha}" LIMIT 1'
    
    #retorna o USUÁRIO se encontrou usuario e senha iguais:
    retorno = executar_comando("GET", comando)
    
    if retorno:
        return jsonify(retorno), 201
    else:
        return {"Status": 'erro ao executar login'}, 400

@user_routes.route('/addFunds', methods=['PUT'])
def add_founds():
    
    user_id = request.headers.get('id')

    

    #verifica se o usuário está autenticado (True ou False)
    if is_authenticated(user_id):

        data = request.json

        #dados sobre o cartão de crédito
        numero = data.get('numero')
        nome = data.get('nome')
        data_vencimento = data.get('data_vencimento')
        cvc = data.get('cvc')
        valor = Decimal(data.get('valor'))

        print(f'numero:{numero}\n nome:{nome}\n data_vencimento:{data_vencimento}\n cvc:{cvc}\n valor:{valor}')

        if numero != "" and nome != "" and data_vencimento != "" and cvc != "" and valor != "":

            comando = f'SELECT wallet_id FROM Carteira WHERE user_id_dono = "{user_id}"'
            wallet_id = executar_comando("GET_BY_ID", comando)

            comando = f'SELECT saldo FROM Carteira WHERE wallet_id = {wallet_id}'
            saldo_atual = executar_comando("GET_BY_ID", comando)

            novo_saldo = saldo_atual + valor

            comando = f'UPDATE Carteira SET saldo = {novo_saldo} WHERE wallet_id = {wallet_id}'
            retorno = executar_comando("PUT", comando)
            
            comando = f'''
                UPDATE Carteira 
                SET historico_compras_creditos = JSON_ARRAY_APPEND(historico_compras_creditos, '$', JSON_OBJECT('Compra de crédito', {valor}))
                WHERE wallet_id = {wallet_id};
                '''
            retorno = executar_comando("PUT", comando)

            if retorno == "sucesso":
                return {'Sucesso': f'O saldo da sua carteira foi atualizado com sucesso para [R$:{novo_saldo}]'}, 201
            else:
                return {'Erro': 'Erro ao atualizar o saldo da sua carteira'}, 404
        else:
            return {'Erro': 'Dados incorretos!'}, 404
    else:
        return {'Erro': 'Usuário não autenticado!'}, 404

@user_routes.route('/withdrawFunds', methods=['PUT'])
def withdraw_founds():

    user_id = request.headers.get('id')

    if is_authenticated(user_id):

        data = request.json
        
        #Coletar dados da requisição
        data_tentativa_de_saque = data.get('data')
        opcao_saque_bool = data.get('opcao') # 0 - BANCO 1 - PIX
        nome_banco = data.get('banco')
        agencia = data.get('agencia')
        conta = data.get('conta')
        digito = data.get('digito')
        chave_pix = data.get('pix')
        valor_de_saque = data.get('valor')

        #Validando se os dados estão incompletos
        if opcao_saque_bool == 0: # BANCO
            if nome_banco == "" or agencia == "" or conta == "" or digito == "":
                return {'Erro': 'Preencha todos os dados da conta bancária'}, 400
            
        elif opcao_saque_bool == 1: # PIX
            if chave_pix == "":
                return {'Erro': 'Preencha todos os dados para chave PIX'}, 400
        
        #Validando se o valor de saque está dentro da faixa permitida
        if valor_de_saque < 1000 or valor_de_saque > 101000.00:
            return {'Erro': 'Valor de saque deve estar entre 1.000,00 e 101.000,00'}, 400

        #Obter wallet_id deste usuario:
        comando = f'SELECT wallet_id FROM Carteira WHERE user_id_dono = "{user_id}"'
        wallet_id = executar_comando("GET_BY_ID", comando)

        #Obter saldo deste usuario:
        comando = f'SELECT saldo FROM Carteira WHERE wallet_id = {wallet_id}'
        saldo = executar_comando("GET_BY_ID", comando)

        ##### LÓGICA PARA SAQUE #####
        comando = f'SELECT data_ultimo_saque FROM Carteira WHERE wallet_id = {wallet_id}'
        data_ultimo_saque_carteira = executar_comando("GET_BY_ID", comando)

        if str(data_ultimo_saque_carteira) != str(data_tentativa_de_saque):

            if valor_de_saque >= 1000.00 and valor_de_saque <= 5000.00: #sacar com taxa de 2%
                valor_de_saque_com_taxa = valor_de_saque + (valor_de_saque * 0.02)
                
            elif valor_de_saque > 5000.00 and valor_de_saque <= 101000.00: #sacar com taxa de 1%
                valor_de_saque_com_taxa = valor_de_saque + (valor_de_saque * 0.01)
            
            
            if valor_de_saque_com_taxa > saldo:
                return {'Erro': 'Saldo indisponível (considerando a taxa de saque)'}, 400
                
            #Atualizar valor de saque acumulado no dia para o valor do saque atual (pois é o primeiro saque do dia)
            comando = f'UPDATE Carteira SET valor_acumulado_saques_diarios = {valor_de_saque_com_taxa} WHERE wallet_id = {wallet_id}'
            retorno = executar_comando("PUT", comando)

            #Atualiza data para dia atual da requisição
            comando = f'UPDATE Carteira SET data_ultimo_saque = "{data_tentativa_de_saque}" WHERE wallet_id = {wallet_id}'
            retorno = executar_comando("PUT", comando)

            #Realizar saque
            novo_saldo = saldo - Decimal(valor_de_saque_com_taxa)

            comando = f'UPDATE Carteira SET saldo = {novo_saldo} WHERE wallet_id = {wallet_id}'
            retorno = executar_comando("PUT", comando)

            return {'Sucesso': 'Saque realizado com sucesso (considerando a taxa de saque)'}, 200 
        
        else: #é o mesmo dia
            
            #Calcular quanto será sacado (com taxa)
            if valor_de_saque > 0 and valor_de_saque <= 100.00: #sacar com taxa de 4%
                valor_de_saque_com_taxa = valor_de_saque + (valor_de_saque * 0.04)

            elif valor_de_saque > 101 and valor_de_saque <= 1000.00: #sacar com taxa de 3%
                valor_de_saque_com_taxa = valor_de_saque + (valor_de_saque * 0.03)

            elif valor_de_saque > 1001 and valor_de_saque <= 5000.00: #sacar com taxa de 2%
                valor_de_saque_com_taxa = valor_de_saque + (valor_de_saque * 0.02)
                
            elif valor_de_saque > 5001 and valor_de_saque <= 101000.00: #sacar com taxa de 1%
                valor_de_saque_com_taxa = valor_de_saque + (valor_de_saque * 0.01)

            comando = f'SELECT valor_acumulado_saques_diarios FROM Carteira WHERE wallet_id = {wallet_id}'
            valor_acumulado_saques_diarios = executar_comando("GET_BY_ID", comando) 
          
            #Verificar se o valor de saque ultrapassa valor permitido por dia
            if Decimal(valor_de_saque_com_taxa) + valor_acumulado_saques_diarios > 101000.00:
                return {'Erro': 'O valor limite de saque diário foi atingido'}, 400
            
            elif Decimal(valor_de_saque_com_taxa) > saldo:
                return {'Erro': 'Saldo indisponível (considerando a taxa de saque)'}, 400
            
            else:
                # Atualiza valor acumulado
                novo_valor_acumulado = Decimal(valor_de_saque_com_taxa) + Decimal(valor_acumulado_saques_diarios)

                comando = f'UPDATE Carteira SET valor_acumulado_saques_diarios = {novo_valor_acumulado} WHERE wallet_id = {wallet_id}'
                executar_comando("PUT", comando)

                #Realizar saque
                novo_saldo = saldo - Decimal(valor_de_saque_com_taxa)

                comando = f'UPDATE Carteira SET saldo = {novo_saldo} WHERE wallet_id = {wallet_id}'
                executar_comando("PUT", comando)

                return {'Sucesso': 'saque realizado com sucesso (considerando a taxa de saque)'}, 200
    else: 
        return {'Erro': 'Usuário precisa estar autenticado'}, 400


@user_routes.route('/saldoWallet', methods=['GET'])
def saldo_wallet():
     
    user_id = request.headers.get('id')

    comando = f'SELECT saldo FROM Carteira WHERE user_id_dono = {user_id}'

    retorno = executar_comando("GET", comando)


    if retorno:
        saldo = retorno[0][0]
        return jsonify({"saldo": float(saldo)}), 200
    else:
        return {"Status": 'erro ao mostrar saldo'}, 400



@user_routes.route('/historicoWallet', methods=['GET'])
def historico_wallet():

    user_id = request.headers.get('id')

    comando = f'SELECT wallet_id FROM Carteira WHERE user_id_dono = "{user_id}"'
    wallet_id = executar_comando("GET_BY_ID", comando)
    
    comando = f'SELECT historico_compras_creditos FROM Carteira WHERE   wallet_id = { wallet_id}'
    compras_creditos = executar_comando("GET_BY_ID", comando)

    comando = f'SELECT historico_creditos_apostados FROM Carteira WHERE  wallet_id = { wallet_id}'
    historico_apostas = executar_comando("GET_BY_ID", comando)
    

    return jsonify({
        "comprasCredito": compras_creditos,
        "valoresApostados": historico_apostas
    })








 

    