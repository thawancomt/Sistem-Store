from flask import  Blueprint, render_template, request, redirect, url_for, flash, g

from flask_login import current_user

from ..services.StockServices import StockServices, datetime, ArticlesService
from ..services.StockChart import StockChart

# services


stock = Blueprint('stock', __name__,
                  template_folder='../templates',
                  url_prefix='/stock',
                  static_folder='../static')

@stock.route('/')
def index():
    stock_page = request.args.get('page', 1, type=int)
    reference_stock = request.args.get('reference_stock', 0)
    
    
    how_many_days_for_chart = request.args.get('days', 4, type=int)
    
    date =  request.args.get('date') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    chart = StockChart(days=how_many_days_for_chart)
    
    default_last_stock_date = request.args.get('date') or (StockServices().get_stocks_dates()[-1].date if StockServices().get_stocks_dates() else None) or g.date
   
    
    context = {
        'title': 'Stock',
        'stock' : StockServices(date=date).get_data_for_stock_total(),
    
        'stocks_data_for_info_table' : StockServices(date=date).create_data_for_stock_table(),
        'articles' : ArticlesService.get_all_stockable(),
        'dates' : StockServices().get_stocks_dates(),
        'reference_stock' : StockServices(date=reference_stock).get_data_for_stock_total(),
        'default_last_date' : default_last_stock_date,
        'default_last_stock' : StockServices(date=default_last_stock_date).get_data_for_stock_total(),
        
        'date_labels' : chart.create_date_labels(),
        'data_for_chart' : chart.create_datasets(),

    }
    #return f'{context['stocks_data_for_info_table']}'
    
    return render_template('stock.html', context=context, date=date, datetime=datetime)  

@stock.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    date = request.args.get('date')
    
   
    StockServices().create_stock(data=data)
    
    return redirect(url_for('stock.index', date=date))
    
    