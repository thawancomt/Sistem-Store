

var ctx = document.getElementById('myChart');
var type = document.getElementById('changeChartType');

var options = {
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
          },
          title:{
            display: true,
            text: 'Stock Chart'
          },
          datalabels: {
            display : false
          }

        },
        scales: {
          y: {
            beginAtZero: true,
            
            
          }
        },
        responsive: true,
        maintainAspectRatio: false,
        onResize : function(chart) {
          chart.update();
        },
        

}



var StockChart = new Chart(ctx, {
  type: type.value,
  data: {
    labels: labels,
    datasets: data,
  },
  options: options
});


function updateChartType(newType) {
  StockChart.destroy(); // Destroi o gráfico atual
  StockChart = new Chart(ctx, { // Cria um novo gráfico com o novo tipo
    type: newType,
    data: {
      labels: labels,
      datasets: data,
    },
    options: options
  });
}

document.getElementById('changeChartType').addEventListener('change', function(chart) {
  const newType = this.value;
  updateChartType(newType);
  
});

