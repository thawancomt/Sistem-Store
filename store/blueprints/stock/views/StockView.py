from store.utils import *
from store.extensions import *

from ..services.StockServices import StockServices, datetime, ArticlesService
from ..services.StockChart import StockChart

""" stock = Blueprint('stock', __name__,
                  template_folder='../templates',
                  url_prefix='/stock',
                  static_folder='../static')

@stock.route('/')
@login_required
def index():
    # pass a date or get the current date
    DateArg : datetime = datetime.strptime(request.args.get('date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
    
    # We want the last stock date to system use 
    # We dont need to treat the case where there is no stock in the system because the system will give us the actual data as a stock if no stock is found
    LastStockDefault : datetime = StockServices(date=DateArg).get_stocks_dates()[-1]
    ReferenceStock : datetime = datetime.strptime(request.args.get('reference_stock', datetime.now().strftime("%Y-%m-%d")), '%Y-%m-%d')

    # Classes
    Chart : StockChart = StockChart(date=DateArg)
    StockService : StockChart = StockServices(date=DateArg)

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
 """

class StockViewBlueprint(BlueprintBase):
    def __init__(self, name=None, static_folder=None, url_prefix=None, template_folder=None, import_name=None,) -> None:
        super().__init__(name, static_folder, url_prefix, template_folder, import_name)
        self.register_routes()
    
    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.blueprint.add_url_rule('/create', 'create', self.create, methods=['POST'])
    
    @login_required
    def index(self):
        # pass a date in URL as a arg or get the actual date, because of our pattern we need to convert the date to a datetime object read: PATTERNS.md
        DateArg : datetime = datetime.strptime(request.args.get('date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
        
        # Here we want to get the last stock in the system based on the date passed in the URL, if not passed we get the last stock in the system
        # The last stock in the system always will be the last stock in the system if database is empty the system will give us the actual date as a stock
        LastStockDefault : datetime = StockServices(date=DateArg).get_stocks_dates()[-1]

        # Here we want to get the reference stock in the system based on the date passed in the URL, if not passed we get the last stock in the system
        # This is used to compare the lastest stock in the system with the stock in the reference date
        ReferenceStock : datetime = datetime.strptime(request.args.get('reference_stock', datetime.now().strftime("%Y-%m-%d")), '%Y-%m-%d')

        # Classes
        Chart : StockChart = StockChart(date=DateArg)
        StockService : StockChart = StockServices(date=DateArg)

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

        return render_template('stock.html', context=context, date=DateArg, datetime=datetime)´
    
    @fresh_login_required
    def create(self):
        StockDataForm : dict[str, str] = request.form.to_dict()

        date = StockDataForm.get('date')

        StockServices().create_stock(data=StockDataForm, date=date)


        return redirect(url_for('stock.index', date=date))
    
    def update(self):
        pass


    def delete(self):
        pass

StockViewBlueprint = StockViewBlueprint(name='stock', import_name=__name__, template_folder='../templates', static_folder='../static', url_prefix='/stock').blueprint
    