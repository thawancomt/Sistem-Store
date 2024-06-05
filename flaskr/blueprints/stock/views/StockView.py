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
    date = request.args.get('date') or stocks[0].date.strftime('%Y-%m-%d %H:%M:%S') if stocks else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    
    context = {
        'title': 'Stock',
        'stock' : StockServices(date=date).get_data_for_stock_total(),
        'stocks_data_for_info_table' : StockServices(date=date).create_data_for_stock_table(),
        'articles' : ArticlesService.get_all_stockable(),
        'dates' : StockServices().get_stocks_dates(),
        
        'date_labels' : StockChart().create_date_labels(),
        'data_for_chart' : StockChart().create_datasets(),
        

    }
    #return f'{context['stocks_data_for_info_table']}'
    
    return render_template('stock.html', context=context, date=date, datetime=datetime)  

@stock.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    StockServices().create_stock(data=data)
    
    return redirect(url_for('stock.index', date = data.get('date')))
    
    