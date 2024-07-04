const ctx = document.getElementById('myChart');

const productionLabels = Array.from(labels)

const selectLimit = document.getElementById('limit')

const newLine = Array.from(dataset)

// Clonando os arrays originais
const originalLabels = Array.from(dataset.labels);
const originalDatasets = dataset.datasets.map(data => ({
    ...data,
    data: Array.from(data.data)
}));

const productionChart = new Chart(ctx, {
    type: 'line',
    data: dataset,
    options: {
        plugins: {
            title : {
                text : 'Production History',
                display : true,
                font : {
                    size : 20
                }
            },
        },
        maintainAspectRatio: false,
        responsive: true
    },
});

// Extensão do protótipo do Chart para limitar os dias
Chart.prototype.limitDays = function(days) {
    // Verificar se o número de dias solicitado é maior do que o número total de labels
    if (days > originalLabels.length) {
        this.data.labels = Array.from(originalLabels);
        // this.data.datasets.forEach((dataset, index) => {
        //     dataset.data = Array.from(originalDatasets[index].data);
        // });
    } else {
        // Fatiar os labels para manter apenas os últimos 'days' labels
        this.data.labels = originalLabels.slice(-days);
        
        // Fatiar os dados em cada dataset para corresponder aos labels
        this.data.datasets.forEach((dataset, index) => {
            dataset.data = originalDatasets[index].data.slice(-days);
        });
    }

    // Atualizar o gráfico para refletir as mudanças
    
}

// Event listener para alterar o número de dias visualizados
selectLimit.addEventListener('change', () => {
    productionChart.limitDays(selectLimit.value);
    productionChart.update();
});
