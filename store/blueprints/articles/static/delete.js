const deleteBtn = document.getElementById('deleteBtn')

deleteBtn.addEventListener('click', () => {
    alert('Proceed with caution!')
    let conf = confirm('Are you sure you want to delete this article?')

    if (conf) {
        deleteBtn.form.submit()
    }
})