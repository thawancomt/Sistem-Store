const createBtn = $('#createBtn')
const orderForm = $('#orderForm')

createBtn.on({
    'click' : () => {
        let confirmation = confirm('Do you want to create this order?')
        if (confirmation) {
            orderForm.submit()
        }
    }
})