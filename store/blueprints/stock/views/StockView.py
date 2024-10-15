from flask import  Blueprint, render_template, request, redirect, url_for, flash, g

from flask_login import current_user, fresh_login_required, login_required

from ..services.StockServices import StockServices, datetime, ArticlesService
from ..services.StockChart import StockChart





stock = Blueprint('stock', __name__,
                  template_folder='../templates',
                  url_prefix='/stock',
                  static_folder='../static')

@stock.route('/')
@login_required
def index():
    ReferenceStock = request.args.get('reference_stock', 0)
    
    DateArg = request.args.get('date') or datetime.now().strftime("%Y-%m-%d")
    
    Chart = StockChart(date=DateArg)

    LastStockDefault = (StockServices().get_stocks_dates()[-1].date if StockServices().get_stocks_dates() else None) or DateArg  

    return str(LastStockDefault)

    
   
    stock_service = StockServices(date=date)
    
    context = {
        'title': 'Stock',
        'stock' : stock_service.get_data_for_stock_total(),
    
        'stocks_data_for_info_table' : stock_service.create_data_for_stock_table(),
        'articles' : ArticlesService.get_all_stockable(),
        'dates' : stock_service.get_stocks_dates(),
        'reference_stock' : StockServices(date=reference_stock).get_data_for_stock_total(),
        'default_last_date' : default_last_stock_date,
        'default_last_stock' : StockServices(date=default_last_stock_date).get_data_for_stock_total(),
        
        'date_labels' : chart.create_date_labels(),
        'data_for_chart' : chart.create_datasets(),

    }

    # return context['data_for_chart']
    
    return render_template('stock.html', context=context, date=date, datetime=datetime)  

@stock.route('/create', methods=['POST'])
@fresh_login_required
def create():

    StockDataForm : dict[str, str] = request.form.to_dict()

    date = StockDataForm.get('date')

    StockServices().create_stock(data=StockDataForm, date=date)


    return redirect(url_for('stock.index', date=date))

@stock.route('/chart', methods=['get'])
@fresh_login_required
def chart():
    StockServices().create_random_stock()
    return redirect(url_for('stock.index'))
    
    