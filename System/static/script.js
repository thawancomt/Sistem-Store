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

const consumeChart = document.getElementById('consumeChart')
                
new Chart(ctx, {
  type: 'line',
  data: {
    labels: dates,
    datasets: data_labels,
    
  },
  options: {
    tension: 0.16,
    pointHoverBackgroundColor: true,
    fill: false,
    spanGaps: true,
    scales: {
      y:{
        beginAtZero: true
      }
      
    }
    
  },
  
});

new Chart(consumeChart, {
  type: 'bar',
  data: {
    labels: consumeWorkers,
    datasets: consumeData
  },
  options: options
});


var options = {
  maintainAspectRatio: false,
  scales: {
    y: {
      stacked: true,
      grid: {
        display: true,
        color: "rgba(255,99,132,0.2)"
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
};