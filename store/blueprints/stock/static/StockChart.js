

var ctx = document.getElementById('myChart');
const type = document.getElementById('changeChartType');

const hideLabels = document.getElementById('hideLabels')

const hideLabelsLabel = document.getElementById('chartDaysLabel')
const daysToChart = document.getElementById('changeHowManyDaysOnChart')

var canvasDiv = document.getElementById('chartDiv');

const labelsfor_chart = Array.from(labels)

const chartInfo = document.getElementById('chart-info')


var options = {
        
        responsive: true,
        maintainAspectRatio: false,
};


var StockChart = createChart('bar');

function createChart(type) {
  return new Chart(ctx, {
    type: type,
    data: {
          labels: labels,
          datasets: data,
      },
      options: options

  })
}

Chart.prototype.hideX = function() {
  this.options.scales.x.display = this.options.scales.x.display ? false : true;
  hideLabels.innerText = this.options.scales.x.display ? 'Hide Labels' : 'Show labels'
  this.update();
};

Chart.prototype.limitDays = function(days) {
  if (days > this.data.labels.length) {
    this.data.labels = Array.from(labelsfor_chart)
  }
    this.data.labels = this.data.labels.slice(-days)
  this.update()
}

hideLabels.addEventListener('click',() => {
  StockChart.hideX()
})



function updateChartType(newType) {
  // Destroy the existing chart instance
  StockChart.destroy()
  StockChart = createChart(newType)
  StockChart.data.labels = Array.from(labelsfor_chart)
  
  canvasDiv.showChart()
}

document.getElementById('changeChartType').addEventListener('change', function(chart) {
  const newType = this.value;
  updateChartType(newType);
  
});

daysToChart.addEventListener('change', () => {
  var days = daysToChart.value
  StockChart.limitDays(days)
})


canvasDiv.showChart = function() {
  StockChart.update()
}
