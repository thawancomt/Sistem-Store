from flask import  Blueprint, render_template, request, redirect, url_for, flash

from flask_login import current_user

from ..services.StockServices import StockServices, datetime, ArticlesService
from ..services.StockChart import StockChart

# services


stock = Blueprint('stock', __name__,
                  template_folder='../templates',
                  url_prefix='/stock')

@stock.route('/')
def index():
    stocks = StockServices().get_stocks_dates()
    date = request.args.get('date')  or stocks[-1].date.strftime('%Y-%m-%d %H:%M:%S') if stocks else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Latest stock
    
    context = {
        'title': 'Stock',
        'stock' : StockServices(date=date).get_data_for_stock_total(), 
        'articles' : ArticlesService.get_all(),
        'dates' : StockServices().get_stocks_dates(),
        
        'date_labels' : StockChart().create_date_labels(),
        'data_for_chart' : StockChart().create_datasets(),
        

    }
    
    return render_template('stock.html', context=context, date=date)  

@stock.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    
    stock = StockServices().create_stock(data=data)
    
    
    return redirect(url_for('stock.index'))