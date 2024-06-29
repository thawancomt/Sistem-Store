const saveBtn = document.getElementById('saveBtn')


saveBtn.addEventListener('click', () => {
    let conf = confirm('Are you sure you want to save changes?')
    if (conf) {
        saveBtn.form.submit()
    }
})