

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
          }
        },
        scales: {
          y: {
            beginAtZero: true,
          },
          x: {
          },
        },
        responsive: true,
        maintainAspectRatio: true,
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
  // Destroy the existing chart instance
  StockChart.destroy();
  
  StockChart = new Chart(ctx, {
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

