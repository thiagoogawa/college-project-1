document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');

    searchButton.addEventListener('click', () => {
        const palavra = searchInput.value.trim(); // Remove espaços desnecessários

        // Redireciona para a página apostar com a palavra como parâmetro
        if (palavra) {
            window.location.href = `http://localhost:5000/events/apostarEvents?search=${encodeURIComponent(palavra)}`;
        } else {
            window.location.href = `http://localhost:5000/events/apostarEvents`; // Vai para a página sem filtro se o campo estiver vazio
        }
    });
});
//--------------------------------------------------------------------------------------------------------------------------
//--------------------------------------------------------------------------------------------------------------------------

//categorias

document.addEventListener('DOMContentLoaded', () => {
    // Adicionar eventos de clique às categorias
    const categorias = document.querySelectorAll('.categorias-card');
    categorias.forEach(categoria => {
        categoria.addEventListener('click', () => {
            const category = categoria.querySelector('p').textContent.trim();
            applyFilterAndRedirect(category);
        });
    });
});

function applyFilterAndRedirect(category) {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        alert('Usuário não autenticado.');
        window.location.href = '/login.html';
        return;
    }
    // Redireciona para a página de apostar com o parâmetro de busca
    const url = `http://localhost:5000/events/apostarEvents?search=${encodeURIComponent(category)}`;
    window.location.href = url;
}
 
//---------------------------------------------------------------------------------------------
//--------------------------------------------------------------------------------------------

//aviso de adicionar saldo

document.addEventListener('DOMContentLoaded', () => {
    const userId = localStorage.getItem('userId');

    if (!userId) {
        alert('Usuário não autenticado.');
        window.location.href = '/login.html';
        return;
    }

    // Função para exibir o alerta
    function exibirAlerta() {
        const desejaAdicionarSaldo = confirm("Deseja adicionar saldo?");
        if (desejaAdicionarSaldo) {
            // Redireciona para a página de adicionar saldo
            window.location.href = "http://localhost:5000/users/addFundsForm";
        } else {
            // Permanece na página atual
            console.log("Usuário escolheu permanecer na página.");
        }
    }

    // Exibe o alerta apenas uma vez por sessão
    if (!sessionStorage.getItem("saldoAlertado")) {
        exibirAlerta();
        sessionStorage.setItem("saldoAlertado", "true"); // Marca que o alerta foi exibido
    }
});
