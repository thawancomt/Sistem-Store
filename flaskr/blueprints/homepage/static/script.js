
const delete_btn = document.getElementById('delete_btn');
const finish_btn = document.getElementById('finish_btn');

function confirmAction(msg, form = NaN) {
    return function() {
        let confirmIt = confirm(msg);
        if (confirmIt) {
            form.submit();
        }
    };
}
delete_btn.addEventListener('click', confirmAction('Confirmathe deletion of task?', delete_btn.form));
finish_btn.addEventListener('click', confirmAction('Confirm the finish of task?', finish_btn.form));
