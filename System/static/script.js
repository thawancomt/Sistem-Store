let btnProduction = document.querySelector('#submit-production-btn');

let productionForm = document.querySelector('#production-form');

function enterProduction () {
    var result = window.confirm("Confirm the amount production?");

    return result
}

btnProduction.addEventListener('click', function() {
    if (enterProduction()) {
        productionForm.submit();
    }
})