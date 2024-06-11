

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
        scaleShowLabels : false
        },
        scales: {
          y: {
            beginAtZero: true,
          },
          x: {
          },
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
  
  StockChart.config.type = newType;
  StockChart.update();
}

document.getElementById('changeChartType').addEventListener('change', function(chart) {
  const newType = this.value;
  updateChartType(newType);
  
});

