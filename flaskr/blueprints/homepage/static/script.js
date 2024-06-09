// Seleciona os botões pelo ID
const delete_btn = document.getElementById('delete_btn');
const finish_btn = document.getElementById('finish_btn');

// Função que retorna outra função para exibir o alerta
function confirmAction(msg) {
    return function() {
        let confirmIt = confirm(msg);
        if (confirmIt) {
            FormData.submit();
            // Aqui você pode adicionar a lógica para realizar a ação, como enviar o formulário
        }
    };
}

// Adiciona um evento de clique a cada botão
delete_btn.addEventListener('click', confirmAction('Confirmathe deletion of task?'));
finish_btn.addEventListener('click', confirmAction('Confirm the finish of task?'));
