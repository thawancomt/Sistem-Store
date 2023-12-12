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
  type: 'line',
  data: {
    labels: dates,
    datasets: [
    {
      label: 'Big Ball',
      data: big,
      
      borderWidth: 3,
    },
    {
        label : 'Small Ball',
        data: small,
        borderWidth: 3,
    },
    {
        label : 'Garlic Bread',
        data: garlic,
        borderWidth: 3,
    },
    {
        label : 'Mozzarela',
        data: mozzarela,
        borderWidth: 3,
        
    },
    {
        label : 'Edamer',
        data: edamer,
        borderWidth: 3,
        
    },
],
    
  },
  options: {
    tension: 0.16,
    pointHoverBackgroundColor: true,
    fill: false,
    spanGaps: true,
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});