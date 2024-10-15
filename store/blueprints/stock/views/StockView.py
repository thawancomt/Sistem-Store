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
    # pass a date or get the current date
    DateArg = datetime.strptime(request.args.get('date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
    
    # We want the last stock date to be the default last stock date
    LastStockDefault = StockServices(date=DateArg).get_stocks_dates()[-1]
    ReferenceStock = datetime.strptime(request.args.get('reference_stock', datetime.now().strftime("%Y-%m-%d")), '%Y-%m-%d')

    # Classes
    Chart = StockChart(date=DateArg)
    StockService = StockServices(date=DateArg)

    context = {
        'title': 'Stock',
        'stock': StockService.get_data_for_stock_total(),
        'stocks_data_for_info_table': StockService.create_data_for_stock_table(),
        'articles': ArticlesService.get_all_stockable(),
        'dates': StockService.get_stocks_dates(),
        'reference_stock': StockServices(date=ReferenceStock).get_data_for_stock_total(),
        'default_last_stock': StockServices(date=LastStockDefault).get_data_for_stock_total(),
        'date_labels': Chart.create_date_labels(),
        'data_for_chart': Chart.create_datasets(),
    }

    return render_template('stock.html', context=context, date=DateArg, datetime=datetime)

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
    
    