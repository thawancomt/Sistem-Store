const ctx = document.getElementById('myChart');

const productionLabels = Array.from(labels)

const selectLimit = document.getElementById('limit')

const newLine = Array.from(dataset)




const productionChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: dataset,
    },
    options: {
        
        maintainAspectRatio : false,
        responsive: true
    },
})

Chart.prototype.limitDays = function(days) {
    if (days > this.data.labels.length) {
      this.data.labels = Array.from(productionLabels)
    }
      this.data.labels = this.data.labels.splice(-days)
    this.update()
  }


selectLimit.addEventListener('change', () => {
    productionChart.limitDays(selectLimit.value)
})