
new Chart(ccc, {
    type: 'line',
    data: {
      labels: dates,
      datasets: data_stock
    },
    options: {
        responsive: true,
        borderWidth: 5,
      scales: {
        y: {
          beginAtZero: true
        }
      },
      tension: 0.1,
    pointHoverBackgroundColor: true,
    fill: false,
    spanGaps: true,
    scales: {
      y:{
        beginAtZero: true
      }
      
    }
    
  
  
    }
  });
  