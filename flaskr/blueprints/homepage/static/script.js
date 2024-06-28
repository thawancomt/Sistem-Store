const delete_btns = document.querySelectorAll('#delete_btn');
const finish_btns = document.querySelectorAll('#finish_btn');

function confirmAction(msg, form) {
    return function() {
        let confirmIt = confirm(msg);
        if (confirmIt) {
            form.submit();
        }
    };
}

Array.prototype.forEach.call(delete_btns, function(btn) {
    btn.addEventListener('click', confirmAction('Confirm the deletion of task?', btn.form));
});

Array.prototype.forEach.call(finish_btns, function(btn) {
    btn.addEventListener('click', confirmAction('Confirm the finish of task?', btn.form));
});
