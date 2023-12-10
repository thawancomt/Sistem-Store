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
      data: big
    },
    {
        label : 'Small Ball',
        data: small
    },
    {
        label : 'Garlic Bread',
        data: garlic
    },
    {
        label : 'Mozzarela',
        data: mozzarela
    },
    {
        label : 'Edamer',
        data: edamer
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