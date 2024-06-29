const deleteTaskBtn = document.querySelectorAll('#confirmDelete')

const editTaskBtn = document.querySelectorAll('#confirmEdit')



deleteTaskBtn.forEach((btn) => {
    btn.addEventListener('click', () => {
        let conf = confirm('Are you sure you want to delete this task?')
        if (!conf) {
          return
        }
        btn.form.submit()
    })
}
)

editTaskBtn.forEach((btn) => {
  
    btn.addEventListener('click', () => {
      let conf = confirm('Are you sure you want to edit this task?')
      if (!conf) {
        return
      }
      console.log(btn.form.submit());
    })
}
)
