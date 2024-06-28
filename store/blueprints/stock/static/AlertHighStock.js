// Select all elements with the id "stock_input"
var stockInputs = document.querySelectorAll('#stock_input');

// Loop through each element and add event listener
stockInputs.forEach(function(stockInput) {
    stockInput.addEventListener('input', showValue);
});

function showValue(event) {
    var inputInt = parseInt(event.target.value);
    if (inputInt > 200) {
        var nameOfArticle = document.getElementById(event.target.name + 'Label');
        window.alert('High amount of this ' + nameOfArticle.innerText);
    }
}
