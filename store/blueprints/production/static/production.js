const insertBtn = document.getElementById("insertBtn");

const insertInputs = document.querySelectorAll("#insertAmount");


function checkLetter(elemente) {
    let result = Number(elemente.value)
    if (result) {
        return true;
    } else {
        elemente.value = "";
        elemente.focus();
        return false;
    }
}

insertBtn.addEventListener("click", () => {
    let conf = confirm('Are you sure you want insert a new production')
    if (conf) {
        insertBtn.form.submit();
    }
})

insertInputs.forEach(
    (element) => {
        element.addEventListener('change', () => {
            checkLetter(element);
        })
    }
)