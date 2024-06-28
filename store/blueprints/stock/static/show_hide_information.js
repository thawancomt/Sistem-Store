const showHide = document.getElementById('show_hide_stock_info')
const stockInfo = document.getElementById('stock_info')

showHide.addEventListener('click', () => {
    showHide.innerText = showHide.innerText == 'Show Info' ? 'Hide Info' : 'Show Info'
    if (stockInfo.hasAttribute('hidden')) {
        stockInfo.removeAttribute('hidden')
    } else {
        stockInfo.setAttribute('hidden', true)
    }
})

// All Stock 
const allStockDiv = document.getElementById('all_stock');

// create stock
const createStockDiv = document.getElementById('create_stock');

// compare stock
const compareStockDiv = document.getElementById('compare_stock');

const allDivs = [allStockDiv, createStockDiv, compareStockDiv]


allDivs.forEach( (element) => {
    element.show = function () {
        if (element.classList.contains('hidden')) {
            console.log('teste');
            this.classList.remove('hidden')
        } else {
            this.classList.add('hidden')
        }
    }
})

function showTool(tool) {
    allDivs
}