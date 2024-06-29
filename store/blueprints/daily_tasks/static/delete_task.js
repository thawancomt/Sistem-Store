const tasksBtn = document.querySelectorAll('#confirmDeletetion')

tasksBtn.forEach((btn) => {
    btn.addEventListener('click', () => {
        let conf = confirm('Are you sure you want to delete this task?')
        if (!conf) {
          return
        }
        btn.form.submit()
    })
}
)