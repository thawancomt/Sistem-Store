const editBtn = document.getElementById('edit_btn');

const editForm = document.getElementById('edit_form');

const password = document.getElementById('password');

const userStatusForm = document.getElementById('active_deactive_form')
const userStatusBtn = document.getElementById('active_deactive_btn')

editBtn.addEventListener("click", () => {
    
    (function () {
        if (password.value.length > 0 && password.value.length < 8) {
            alert(`The password must be have more ${8 -password.value.length} characters`)
            return;
        } else {
            const confirm = window.confirm('Confirm the edition');

            if(confirm){
                editForm.submit();
            } else {
                alert('Edition canceled')
            }
            

        }
    })()
    
})
userStatusBtn.addEventListener("click", () => {
    const confirm = window.confirm('Confirm the edition');
    if(confirm){
        userStatusForm.submit();
    } else {
        alert('Edition canceled')
    }
})




function t(msg, form) {
    const confirm = window.confirm('Confirm the edition');
    if(confirm){
        form.submit();
    } else {
        alert('Edition canceled')
    }

}
