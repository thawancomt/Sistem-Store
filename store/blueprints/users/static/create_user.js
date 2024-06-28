const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm_password');

const registerForm = document.getElementById('register_form')

const createBtn = document.getElementById('create_user_btn');



function checkPassword(){
    if (password.value !== confirmPassword.value){
        alert('The password is not the same');
    } else {
        if (!(password.value.length >= 8)) {
            alert('The password must be at least 8 characters long');
            return;
        }
        if (registerForm.checkValidity()) {
            registerForm.submit();
        } else {
            alert('Please fill out all fields');
        }
    }
}

createBtn.addEventListener('click', checkPassword); 