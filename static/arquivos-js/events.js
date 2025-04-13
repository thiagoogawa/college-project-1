// criar eventos
document.addEventListener('DOMContentLoaded', () => {

    const URL_meusEventos = 'http://localhost:5000/events/meusEventos'

    const URL_newEvents = 'http://localhost:5000/events/new';

    const btn_newEvents = document.querySelector("#criar-Evento");

    if (btn_newEvents) {
        btn_newEvents.addEventListener('click', async function (event) {
            event.preventDefault();

            const userId = localStorage.getItem('userId');

            if (!userId) {
                alert('Usuário não autenticado.');
                window.location.href = '/login.html';
                return;
            }

            const title = document.getElementById("title-events").value;
            const descricao = document.getElementById("descricao-events").value;
            const valor_de_cada_cota = parseFloat(document.getElementById("valor_de_cada_cota-events").value);
            const periodo_para_apostar_inicio = document.getElementById("periodo_para_apostar_inicio-events").value;
            const periodo_para_apostar_fim = document.getElementById("periodo_para_apostar_fim-events").value;
            const data_acontecimento = document.getElementById("data_acontecimento-events").value;

            const body = {
                "title": title,
                "descricao": descricao,
                "valor_de_cada_cota": valor_de_cada_cota,
                "periodo_para_apostar_inicio": periodo_para_apostar_inicio,
                "periodo_para_apostar_fim": periodo_para_apostar_fim,
                "data_acontecimento": data_acontecimento
            };

            try {
                const response = await fetch(URL_newEvents, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'id': userId
                    },
                    body: JSON.stringify(body)
                });
                const data = await response.json();
                console.log("Resposta Rota URL_newEvents :", data);

                if (data.Status === 'O valor de cota deve ser superior a R$ 1,00') {
                    alert('O valor de cota deve ser superior a R$ 1,00.');
                } else {
                    alert('Evento criado com sucesso!');
                    window.location.href = URL_meusEventos
                }
            } catch (error) {
                console.error("Erro ao criar evento:", error);
            }
        });
    }
})


//------------------------------------------------------------------------------------

//Meus Eventos

document.addEventListener('DOMContentLoaded', async () => {
    const URL_historicoMeusEventos = 'http://localhost:5000/events/historicoMeusEventos';

    const userId = localStorage.getItem('userId');

    if (!userId) {
        console.error('User ID não encontrado no localStorage');
        return;
    }

    try {
        const response = await fetch(URL_historicoMeusEventos, {
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
        console.log("Resposta do servidor URL_historicoMeusEventos:", data);

        const idDoEvento = document.getElementById('id-do-evento');
        const nomeEvento = document.getElementById('nome-evento');
        const statusEvento = document.getElementById('status-evento');
        const eventBtn = document.getElementById('deletar-evento');


        // Itera sobre os dados recebidos
        data.forEach(item => {
            // Adiciona o id do evento
            const idDoEventoItem = document.createElement('ul');
            idDoEventoItem.textContent = item[0];
            idDoEvento.appendChild(idDoEventoItem);

            // Adiciona o título do evento
            const nomeItem = document.createElement('ul');
            nomeItem.textContent = item[1];
            nomeEvento.appendChild(nomeItem);

            // Adiciona o status do evento
            const statusItem = document.createElement('ul');
            statusItem.textContent = item[2];
            statusEvento.appendChild(statusItem);

            // Cria o botão de deletar
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Deletar';
            deleteButton.classList.add('delete-btn');

            // Adiciona o botão de deletar ao DOM
            eventBtn.appendChild(deleteButton);

            // Adiciona evento de clique no botão de deletar
            deleteButton.addEventListener('click', async () => {
                try {
                    const body = { event_id: item[0] };

                    const deleteResponse = await fetch(`http://localhost:5000/events/${item[0]}/delete`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'id': userId
                        },
                        body: JSON.stringify(body)
                    });

                    const deleteData = await deleteResponse.json();
                    console.log('Resposta da API:', deleteData);

                    if (deleteData.Sucesso) {
                        alert(deleteData.Sucesso);
                        idDoEventoItem.remove(); // Remove o ID do evento
                        nomeItem.remove();       // Remove o nome do evento
                        statusItem.remove();     // Remove o status do evento
                        deleteButton.remove();   // Remove o botão de deletar
                    } else {
                        alert(deleteData.Erro || 'Erro ao deletar evento.');
                    }
                } catch (error) {
                    console.error('Erro ao deletar evento:', error);
                    alert('Erro ao deletar evento. Tente novamente.');
                }
            });

            
        });
    } catch (error) {
        console.error("Erro ao buscar os históricos:", error);
    }
});


//----------------------------------------------------------------------------------------------------------------

//Apostar 
//buscar evento por palavra chave


// Função para criar a estrutura de um evento
function criarEstruturaEvento(evento) {
    const cards = document.createElement('div');
    cards.className = 'cards';

    // Top Card
    const topCard = document.createElement('section');
    topCard.className = 'top-card';

    const idEvento = document.createElement('p');
    idEvento.id = 'id-do-evento';
    idEvento.textContent = `Evento ID: ${evento.event_id}`;

    const nomeEvento = document.createElement('h3');
    nomeEvento.id = 'nome-evento';
    nomeEvento.textContent = evento.title;

    topCard.appendChild(idEvento);
    topCard.appendChild(nomeEvento);

    // Mid Card
    const midCard = document.createElement('section');
    midCard.className = 'mid-card';

    const descricaoEvento = document.createElement('p');
    descricaoEvento.id = 'descricao-evento';
    descricaoEvento.textContent = evento.descricao;

    const datas = document.createElement('section');
    datas.className = 'datas';

    const dataInicio = document.createElement('p');
    dataInicio.id = 'data-inicio-evento';
    dataInicio.textContent = `Início: ${evento.periodo_para_apostar_inicio}`;

    const dataFim = document.createElement('p');
    dataFim.id = 'data-fim-evento';
    dataFim.textContent = `Fim: ${evento.periodo_para_apostar_fim}`;

    const dataAcontecimento = document.createElement('p');
    dataAcontecimento.id = 'data-acontecimento';
    dataAcontecimento.textContent = `Acontece: ${evento.data_acontecimento}`;

    datas.appendChild(dataInicio);
    datas.appendChild(dataFim);
    datas.appendChild(dataAcontecimento);

    midCard.appendChild(descricaoEvento);
    midCard.appendChild(datas);

    // Bottom Card
    const betSection = document.createElement('section');
    const betTitle = document.createElement('h3');
    betTitle.textContent = 'Escolha sua aposta';

    const bottomCard = document.createElement('section');
    bottomCard.className = 'bottom-card';

    const betForm = document.createElement('form');
    betForm.id = 'bet-form';

    const valorCota = document.createElement('p');
    valorCota.id = 'valor-cota';
    valorCota.textContent = `Valor de cada cota: R$${parseFloat(evento.valor_de_cada_cota).toFixed(2)}`;


    const labelQtdCotas = document.createElement('label');
    labelQtdCotas.setAttribute('for', `qtd-cotas-${evento.event_id}`);
    labelQtdCotas.textContent = 'Quantidade de cotas:';

    const inputQtdCotas = document.createElement('input');
    inputQtdCotas.type = 'number';
    inputQtdCotas.id = `qtd-cotas-${evento.event_id}`;
    inputQtdCotas.name = `qtd-cotas-${evento.event_id}`;
    inputQtdCotas.min = '1';
    inputQtdCotas.required = true;

    const betButtonsDiv = document.createElement('div');
    betButtonsDiv.className = 'bet-buttons';

    const btnSim = document.createElement('button');
    btnSim.type = 'button';
    btnSim.id = 'btn-sim';
    btnSim.textContent = 'Sim';
    btnSim.setAttribute('onclick', `bet('sim', ${evento.event_id})`);

    const btnNao = document.createElement('button');
    btnNao.type = 'button';
    btnNao.id = 'btn-nao';
    btnNao.textContent = 'Não';
    btnNao.setAttribute('onclick', `bet('nao', ${evento.event_id})`);

    betButtonsDiv.appendChild(btnSim);
    betButtonsDiv.appendChild(btnNao);

    betForm.appendChild(valorCota);
    betForm.appendChild(labelQtdCotas);
    betForm.appendChild(inputQtdCotas);
    betForm.appendChild(betButtonsDiv);

    bottomCard.appendChild(betForm);

    betSection.appendChild(betTitle);
    betSection.appendChild(bottomCard);

    cards.appendChild(topCard);
    cards.appendChild(midCard);
    cards.appendChild(betSection);

    return cards;
}
//função que pega palavra da caixa de busca da home
function getSearchParameter() {
    const params = new URLSearchParams(window.location.search);
    return params.get('search'); // Obtém o valor do parâmetro 'search'
}

//função que carrega todos eventos, junto com os filtros
async function carregarEventos() {
    const container = document.querySelector('.engloba-cards');
    container.innerHTML = ''; // Limpa os eventos exibidos

    const userId = localStorage.getItem('userId');

    if (!userId) {
        alert('Usuário não autenticado.');
        window.location.href = '/login.html';
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/events/retornaEventos', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'id': userId,
            },
        });

        if (!response.ok) {
            console.error('Erro na requisição:', response.status);
            return;
        }

        const data = await response.json();
        console.log('Resposta da API:', data);

        // Verificando e mapeando os dados para objetos
        const eventos = data.map(evento => {
            return {
                event_id: evento[0],
                title: evento[1],
                descricao: evento[2],
                valor_de_cada_cota: evento[3],
                periodo_para_apostar_inicio: evento[4],
                periodo_para_apostar_fim: evento[5],
                data_acontecimento: evento[6],
            };
        });

        const palavra = getSearchParameter()?.toLowerCase();

        if (palavra) {
            // Filtra os eventos se houver parâmetro de busca
            const eventosFiltrados = eventos.filter(evento =>
                evento.descricao.toLowerCase().includes(palavra) ||
                evento.title.toLowerCase().includes(palavra)
            );
            renderizarEventos(eventosFiltrados); // Renderiza os eventos filtrados
        } else {
            // Se não houver filtro, mostra todos os eventos
            renderizarEventos(eventos);
        }

        // Remover o parâmetro de busca após carregar a página (se ele existir na URL)
        if (palavra) {
            const url = new URL(window.location);
            url.searchParams.delete('search'); // Remove o parâmetro 'search'
            window.history.replaceState({}, '', url.toString()); // Atualiza a URL sem o parâmetro
        }

        adicionarFiltroBusca(eventos); // Função para aplicar o filtro de busca (se necessário)

    } catch (error) {
        console.error('Erro:', error);
    }
}


// Função para renderizar eventos no container
function renderizarEventos(eventos) {
    const container = document.querySelector('.engloba-cards');
    container.innerHTML = ''; // Limpa o container antes de renderizar

    if (eventos.length === 0) {
        container.innerHTML = '<p style="color: #F0F8FF; font-size: 20px;">Nenhum evento encontrado.</p>';
        return;
    }

    eventos.forEach(evento => {
        const estruturaEvento = criarEstruturaEvento(evento);
        container.appendChild(estruturaEvento);
    });
}

// Função para adicionar o filtro de busca
function adicionarFiltroBusca(eventos) {
    const searchInput = document.getElementById('pesquisa-palavra');
    const searchButton = document.getElementById('Buscar');

    searchButton.addEventListener('click', () => {
        const palavra = searchInput.value.toLowerCase();

        if (!palavra) {
            renderizarEventos(eventos); // Mostra todos os eventos se o campo estiver vazio
        } else {
            const eventosFiltrados = eventos.filter(evento =>
                evento.descricao.toLowerCase().includes(palavra) ||
                evento.title.toLowerCase().includes(palavra)
            );
            renderizarEventos(eventosFiltrados);
        }
    });
}

// Função para enviar a aposta
async function bet(opcao, event_id) {
    const atualizaPagina = 'http://localhost:5000/events/apostarEvents'
    const userId = localStorage.getItem('userId');
    const qtdCotas = document.getElementById(`qtd-cotas-${event_id}`).value; // Quantidade de cotas

    try {
        if (!userId) {
            console.error('User ID não encontrado no localStorage');
            return;
        }

        if (!qtdCotas || qtdCotas <= 0) {
            console.error('Por favor, insira uma quantidade válida de cotas.');
            return;
        }

        const dadosAposta = {
            opcao: opcao,
            cotas: parseInt(qtdCotas),
        };

        const response = await fetch(`http://localhost:5000/events/${event_id}/betOnEvent`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'id': userId,
            },
            body: JSON.stringify(dadosAposta),
        });

        const data = await response.json();
        console.log(data)

        
        if (data.Erro === 'Saldo insuficiente para criar aposta!'){
            alert('Saldo insuficiente para criar aposta!')
            window.location.href = atualizaPagina
        }else{
            window.location.href = atualizaPagina
        }

        if (!response.ok) {
            console.error('Erro na requisição ao servidor.');
            return;
        }

    } catch (error) {
        console.error('Erro ao realizar aposta:', error);
        alert(`Erro: ${error.message}`);
    }

    
}

// Inicializar o script quando a página for carregada
document.addEventListener('DOMContentLoaded', () => {
    carregarEventos();
});

//--------------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------------

// eventos proximos de vencer

function estruturaEventoVencimento(evento) {
    // Seleciona o contêiner onde os eventos serão adicionados
    const container = document.querySelector('.destaques-card');

    if (!container) {
        console.error('Elemento .destaques-card não encontrado!');
        return;
    }


    // Cria o campo de lista
    const campoDeLista = document.createElement('ul');
    campoDeLista.className = 'campoLista';

    // Cria o item da lista com informações do evento
    const listaVencimento = document.createElement('li');
    listaVencimento.className = 'listas';
    listaVencimento.textContent = `Nome: ${evento.title} - Término: ${evento.periodo_para_apostar_fim}`;

    // Adiciona o item da lista ao campo de lista
    campoDeLista.appendChild(listaVencimento);

    // Cria um contêiner para juntar o subtítulo e a lista
    const eventoContainer = document.createElement('div');
    eventoContainer.className = 'evento-container';
    eventoContainer.appendChild(campoDeLista);

    // Retorna o contêiner completo (subtítulo + lista)
    return eventoContainer;
}

// Busca eventos próximos ao vencimento no backend
async function retornaEventosVencimento() {
    const container = document.querySelector('.destaques-card');
    container.innerHTML = ''; // Limpa os eventos exibidos

    const userId = localStorage.getItem('userId');

    if (!userId) {
        alert('Usuário não autenticado.');
        window.location.href = '/login.html';
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/events/vencendo', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'id': userId,
            },
        });

        if (!response.ok) {
            console.error('Erro na requisição:', response.status);
            container.innerHTML = '<p>Erro ao carregar eventos. Tente novamente mais tarde.</p>';
            return;
        }

        const data = await response.json();
        console.log('Resposta da API 5:', data);

        // Verifica e mapeia os dados para objetos mais amigáveis
        const eventos = data.map(evento => ({
            event_id: evento[0],
            title: evento[2],
            periodo_para_apostar_fim: evento[6],
        }));

        // Renderiza os eventos
        renderiza(eventos);
    } catch (error) {
        console.error('Erro ao buscar eventos:', error);
        container.innerHTML = '<p>Erro ao carregar eventos. Tente novamente mais tarde.</p>';
    }
}

// Renderiza os eventos na tela
function renderiza(eventos) {
    const container = document.querySelector('.destaques-card');
    container.innerHTML = ''; // Limpa o container antes de renderizar

    if (eventos.length === 0) {
        container.innerHTML = '<p>Nenhum evento encontrado.</p>';
        return;
    }

    eventos.forEach(evento => {
        const estruturaEvento = estruturaEventoVencimento(evento);
        container.appendChild(estruturaEvento);
    });
}

// Adiciona o listener para DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    retornaEventosVencimento();
});


//--------------------------------------------------------------------------------------------
//----------------------------------------------------------------------------------------------

//Mais apostados

// Função para estruturar cada evento mais apostado
function estruturaEventosMaisApostados(evento) {

    
    
    // Cria o contêiner principal para o evento
    const eventoContainer = document.createElement('div');
    eventoContainer.className = 'evento-container';

    // Cria o item da lista com informações do evento
    const listaItem = document.createElement('li');
    listaItem.className = 'listas';
    listaItem.textContent = `ID: ${evento.event_id} - Nome: ${evento.title} - Total de Apostas: ${evento.total_apostas}`;

    // Adiciona o item ao contêiner principal
    eventoContainer.appendChild(listaItem);

    
    // Retorna o contêiner completo
    return eventoContainer;
}

// Função que vai buscar os eventos mais apostados da API
async function retornaEventosMaisApostados() {
    const container = document.querySelector('.destaques-card-mais-votados');
    container.innerHTML = ''; // Limpa o container antes de renderizar

    const userId = localStorage.getItem('userId');

    if (!userId) {
        alert('Usuário não autenticado.');
        window.location.href = '/login.html';
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/events/maisApostados', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'id': userId,
            },
        });

        if (!response.ok) {
            console.error('Erro na requisição:', response.status);
            container.innerHTML = '<p>Erro ao carregar eventos. Tente novamente mais tarde.</p>';
            return;
        }

        const data = await response.json();
        console.log('Resposta da API:', data);

        // Ajuste o mapeamento para corresponder ao formato retornado pela API
        const eventosMaisApostados = data.map(evento => ({
            event_id: evento[0],
            title: evento[1],
            total_apostas:  parseFloat(evento[2]),
        }));

        // Use a função correta para renderizar os eventos
        renderizaMaisApostados(eventosMaisApostados);
    } catch (error) {
        console.error('Erro ao buscar eventos:', error);
        container.innerHTML = '<p>Erro ao carregar eventos. Tente novamente mais tarde.</p>';
    }
}

// Função para renderizar os eventos na tela
function renderizaMaisApostados(eventosMaisApostados) {
    const container = document.querySelector('.destaques-card-mais-votados');
    container.innerHTML = ''; // Limpa o container antes de renderizar

    if (eventosMaisApostados.length === 0) {
        container.innerHTML = '<p>Nenhum evento encontrado.</p>';
        return;
    }

    eventosMaisApostados.forEach(evento => {
        const estruturaEvento = estruturaEventosMaisApostados(evento);

        // Verifica se o retorno é válido antes de adicionar ao container
        if (estruturaEvento instanceof Node) {
            container.appendChild(estruturaEvento);
        } else {
            console.error('Estrutura de evento inválida:', estruturaEvento);
        }
    });
}

// Adiciona o listener para DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    retornaEventosMaisApostados();
});



    



    