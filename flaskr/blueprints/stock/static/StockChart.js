
var ctx = document.getElementById('myChart');
var type = document.getElementById('changeChartType');
var StockChart = new Chart(ctx, {
  type: type.value,
  data: {
    labels: labels,
    datasets: data,
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    },
    responsive: true,
    maintainAspectRatio: false,
  }
});

function updateChartType(newType) {
  StockChart.destroy(); // Destroi o gráfico atual
  StockChart = new Chart(ctx, { // Cria um novo gráfico com o novo tipo
    type: newType,
    data: {
      labels: labels,
      datasets: data,
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      },
      responsive: true,
      maintainAspectRatio: false,
    }
  });
}

document.getElementById('changeChartType').addEventListener('change', function() {
  const selectedType = this.value;
  updateChartType(selectedType);
});

