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

const ctx = document.getElementById('myChart');


                  
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: dates,
    datasets: [
    {
      label: 'Big Ball',
      data: big,
      
      borderWidth: 2,
    },
    {
        label : 'Small Ball',
        data: small,
        borderWidth: 2,
    },
    {
        label : 'Garlic Bread',
        data: garlic,
        borderWidth: 2,
    },
    {
        label : 'Mozzarela',
        data: mozzarela,
        borderWidth: 2,
    },
    {
        label : 'Edamer',
        data: edamer,
        borderWidth: 2,
    },
],
    
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});