//SignUp

document.addEventListener('DOMContentLoaded', () => {

    const URL_loginForm = 'http://localhost:5000/users/loginForm'

    const URL_signUp = 'http://localhost:5000/users/signUp';
    const btn_signUp = document.querySelector("#btn-cadastro");
    if (btn_signUp) {
        btn_signUp.addEventListener('click', async function (event) {
            event.preventDefault();

            const nome = document.getElementById("nome-id").value;
            const cpf = document.getElementById("cpf-id").value;
            const data_nascimento = document.getElementById("data_nascimento-id").value;
            const email = document.getElementById("email-id").value;
            const senha = document.getElementById("pass-id").value;

            const body = {
                "nome": nome,
                "cpf": cpf,
                "data_nascimento": data_nascimento,
                "email": email,
                "senha": senha
            };

            try {
                const response = await fetch(URL_signUp, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(body)
                });
                const data = await response.json();
                console.log("Resposta Rota 8:", data);

                if (data.Status === 'erro ao executar cadastro') {
                    alert('Cadastro falhou. Verifique seus dados.');
                } else {
                    alert('Cadastro realizado com sucesso!');
                    window.location.href = URL_loginForm
                }
            } catch (error) {
                console.error("Erro ao se cadastrar:", error);
            }
        });
    }



});

//--------------------------------------------------------------------------------------------------


//Login

document.addEventListener('DOMContentLoaded', () => {

    const URL_home = 'http://localhost:5000/home'

    const URL_login = 'http://localhost:5000/users/login';
    const bt_login = document.querySelector('#btnLogin');
    if (bt_login) {

        bt_login.addEventListener('click', async function (event) {
            event.preventDefault();

            const email = document.getElementById("email-login").value;
            const senha = document.getElementById("pass-login").value;

            const body = {
                "email": email,
                "senha": senha
            };

            try {
                const response = await fetch(URL_login, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(body)
                });

                const data = await response.json();
                console.log("Resposta Rota 9:", data);

                const userId = data[0][0]; // Acessa o valor '1' no exemplo3

                const userName = data[0][1];
                console.log("userName", userName)

                if (data.Status === 'erro ao executar login') {
                    alert('Login falhou. Verifique seu e-mail e senha.');
                } else {
                    console.log("Sucesso no login");
                    alert('Login realizado com sucesso!');
                    localStorage.setItem('userId', userId);
                    localStorage.setItem('userName', userName);
                    window.location.href = URL_home
                    //localStorage.getItem('userId', userId);
                }
            } catch (error) {
                console.error("Erro ao realizar login:", error);
            }
        });

    }
})



//-----------------------------------------------------------------------------------------------

//addFunds

document.addEventListener('DOMContentLoaded', () => {

    const URL_forCarteira = 'http://localhost:5000/users/minhaWalletForm'

    const URL_addFunds = 'http://localhost:5000/users/addFunds';
    const btn_addFunds = document.querySelector('#btnAddFunds');

    if (btn_addFunds) {
        btn_addFunds.addEventListener('click', async function (event) {
            event.preventDefault();

            const userId = localStorage.getItem('userId');

            if (!userId) {
                alert('Usuário não autenticado.');
                window.location.href = '/login.html';
                return;
            }

            const numero = document.getElementById('numero-id').value;
            const nome = document.getElementById('nome-id').value;
            const data_vencimento = document.getElementById('data_vencimento-id').value;
            const cvc = document.getElementById('cvc-id').value;
            const valor = parseFloat(document.getElementById('valor-id').value);

            const body = {
                "numero": numero,
                "nome": nome,
                "data_vencimento": data_vencimento,
                "cvc": cvc,
                "valor": valor
            };

            try {
                const response = await fetch(URL_addFunds, {
                    method: 'PUT',
                    headers: {
                        'content-Type': 'application/json',
                        'id': userId
                    },
                    body: JSON.stringify(body)
                });

                const data = await response.json();
                console.log("Resposta Rota 10:", data);

                if (data.Status === 'Erro ao atualizar o saldo da sua carteira') {
                    alert('Erro ao atualizar o saldo da sua carteira');
                } else {
                    console.log('O saldo da sua carteira foi atualizado com sucesso');
                    alert('O saldo da sua carteira foi atualizado com sucesso');
                    window.location.href = URL_forCarteira
                }
            } catch (error) {
                console.error("Erro ao adicionar dinheiro:", error);
            }
        });

    }


});



//-------------------------------------------------------------------------------------------------

//Exibir cadastro pelo login
//chamar rota na back que retorna o html da pagina de cadastro
document.addEventListener('DOMContentLoaded', () => {
    const URL_login = 'http://localhost:5000/users/login';

    const URL_signUpForm = 'http://localhost:5000/users/signUpForm';
    const btn_signUpForm = document.querySelector("#btn-chamar-cadastro");
    if (btn_signUpForm) {
        btn_signUpForm.addEventListener('click', async function (event) {
            event.preventDefault();

            window.location.href = URL_signUpForm

        });
    }
});

//------------------------------------------------------------------------------------------------------

//Boas-vindas ao usuário


document.addEventListener('DOMContentLoaded', () => {
    // Verifique se há um valor no localStorage
    const userName = localStorage.getItem('userName');

    // Se o nome do usuário estiver armazenado, exiba-o na página
    if (userName) {
        document.getElementById('user-name').innerText = `Bem-vindo(a) ${userName}`;
    } else {
        // Se não houver nome armazenado, talvez você queira exibir uma mensagem padrão ou redirecionar
        document.getElementById('user-name').innerText = "Nome não encontrado";
    }
});

//-------------------------------------------------------------------------------------------------------------------

//atualiza saldo na tela

document.addEventListener('DOMContentLoaded', async () => {
    const URL_carteira = 'http://localhost:5000/users/saldoWallet';

    // Recuperando o user_id do localStorage
    const userId = localStorage.getItem('userId'); // Substitua 'user_id' com a chave que você usou para armazenar o ID

    if (!userId) {
        console.error('User ID não encontrado no localStorage');
        return;
    }

    try {
        const response = await fetch(URL_carteira, {
            method: 'GET',
            headers: {
                'content-Type': 'application/json',
                'id': userId
            }
        });

        if (!response.ok) {
            console.error('Erro na requisição:', response.status);
            return;
        }

        const data = await response.json();

        // Exibe o saldo se estiver presente na resposta
        if (data.saldo) {
            const saldo = data.saldo;
            document.querySelector('#saldo').innerText = `R$ ${saldo.toFixed(2)}`;
        } else {
            console.error('Saldo não encontrado ou não é um número válido');
        }

    } catch (error) {
        console.error("Erro ao buscar o saldo:", error);
    }
});

//------------------------------------------------------------------------------------------------------

//sacar dinheiro

document.addEventListener('DOMContentLoaded', () => {

    const URL_sacar_fundo = 'http://localhost:5000/users/withdrawFunds';
    const URL_for_sacar_fundo = 'http://localhost:5000/users/withdrawForm';

    const btn_sacar_fundo = document.querySelector('#btnWithdraw');

    if (btn_sacar_fundo) {
        btn_sacar_fundo.addEventListener('click', async function (event) {
            event.preventDefault();

            const userId = localStorage.getItem('userId');

            if (!userId) {
                alert('Usuário não autenticado.');
                window.location.href = '/login.html';
                return;
            }

            const data_tentativa_de_saque = document.getElementById('data-id').value;
            const opcao_saque_bool = parseInt(document.getElementById('opcao-id').value, 10);
            const nome_banco = document.getElementById('banco-id').value;
            const agencia = document.getElementById('agencia-id').value;
            const conta = document.getElementById('conta-id').value;
            const digito = document.getElementById('digito-id').value;
            const chave_pix = document.getElementById('pix-id').value;
            const valor_de_saque = parseFloat(document.getElementById('valor-id').value);

            const body = {
                "data": data_tentativa_de_saque,
                "opcao": opcao_saque_bool,
                "banco": nome_banco,
                "agencia": agencia,
                "conta": conta,
                "digito": digito,
                "pix": chave_pix,
                "valor": valor_de_saque

            };

            try {
                const response = await fetch(URL_sacar_fundo, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'id': userId
                    },
                    body: JSON.stringify(body)
                });

                const data = await response.json();
                console.log("Resposta do servidor:", data);

                if (data.Status === 'Erro ao atualizar saque') {
                    alert('Erro ao realizar saque');
                } else {
                    console.log('Saque realizado com sucesso');
                    alert('Saque realizado com sucesso');
                    window.location.href = URL_for_sacar_fundo;
                }
            } catch (error) {
                console.error("Erro ao realizar o saque:", error);
                alert('Ocorreu um erro ao processar seu saque.');
            }
        });

    }





})

//-----------------------------------------------------------------------------------------------------------------------

//historico de compras


document.addEventListener('DOMContentLoaded', async () => {
    const URL_historico = 'http://localhost:5000/users/historicoWallet';
    
    // Recuperando o user_id do localStorage
    const userId = localStorage.getItem('userId');
    
    if (!userId) {
        console.error('User ID não encontrado no localStorage');
        return;
    }

    try {
        const response = await fetch(URL_historico, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'id': userId
            }
        });

        if (!response.ok) {
            console.error('Erro na requisição:', response.status);
            return;
        }

        const data = await response.json();
        console.log("Resposta do servidor:", data);

        
        if (typeof data.comprasCredito === 'string') {
            data.comprasCredito = JSON.parse(data.comprasCredito);
        }

        if (typeof data.valoresApostados === 'string') {
            data.valoresApostados = JSON.parse(data.valoresApostados);
        }

        // Seleciona os elementos das listas
        const comprasCreditoList = document.getElementById('compras-credito');
        const valoresApostadosList = document.getElementById('valores-apostados');

        // Histórico de compras de crédito
        data.comprasCredito.forEach(item => {
            // Obtem nome da primeira chave do objeto
            const nome = Object.keys(item)[0]; // "Compra de crédito"
            const valor = item[nome]; // 100000
        
            const listItem = document.createElement('li');
            listItem.textContent = `${nome}: R$ ${valor}`;
            comprasCreditoList.appendChild(listItem);
        });

        const valoresApostados = data.valoresApostados
        if (valoresApostados.length === 0) {
            
            const aviso = document.createElement('li');
            aviso.textContent = 'Nenhuma aposta realizada';
            valoresApostadosList.appendChild(aviso);

        }else{
            // Histórico de valores apostados
            data.valoresApostados.forEach(item => {
                const nome = Object.keys(item)[0];
                const valor = item[nome];
        
                const listItem = document.createElement('li');
                listItem.textContent = `${nome}: R$ ${valor}`;
                valoresApostadosList.appendChild(listItem);
            });
            
        }
        
    } catch (error) {
        console.error("Erro ao buscar os históricos:", error);
    }
});

//-------------------------------------------------------------------------------------------------------------


// Logout

document.addEventListener('DOMContentLoaded', () => {
    const URL_loginForm = 'http://localhost:5000/users/loginForm'

    const logoutButton = document.querySelector('#logoutButton');

    if(logoutButton){
        logoutButton.addEventListener('click', async () =>{
            localStorage.clear()

            sessionStorage.clear();

            window.location.href = URL_loginForm
        })
    }else {
        console.error('Botão de logout não encontrado.');
    }
})