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

