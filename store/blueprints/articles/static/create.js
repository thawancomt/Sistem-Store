const createBtn = document.getElementById('createBtn')


createBtn.addEventListener('click', () => {
    if (createBtn.parentNode.checkValidity()) {
        let conf = confirm('Are you sure you want to create this article?');
        if (conf) {
            createBtn.form.submit();
        }
    } else {
        alert('Complete the form');
    }
})