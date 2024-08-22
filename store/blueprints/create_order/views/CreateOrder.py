from store.utils import *
from store.extensions import BlueprintBase

from ...articles.services.ArticlesService import ArticlesService
from ...stock.services.StockServices import StockServices

class CreateOrderBlueprint(BlueprintBase):
    def __init__(self, name='orders', import_name=__name__,
                 template_folder='../templates',
                 url_prefix='/orders',
                 static_folder='../static'):
        
        self.blueprint = Blueprint(name, import_name,
                                   template_folder=template_folder,
                                static_folder=static_folder,
                                url_prefix=url_prefix)
        
        self.register_routes()

    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index)

    def index(self):
        stock_dates = StockServices().get_stocks_dates()

        last_stock, before_last_stock = StockServices(date=stock_dates[-1].date).get_stock(), StockServices(date=stock_dates[-2].date).get_stock()

        context = {
            'articles' : ArticlesService().get_all_active(),
            'last_stock' : StockServices().convert_stock_object_to_dict(last_stock),
            'before_last_stock' : StockServices().convert_stock_object_to_dict(before_last_stock),
            'dates' : stock_dates
        }
        return render_template('index.html', context = context)
    def create(self):
        pass
    def update(self):
        pass
    def delete(self):
        pass

CreateOrderBlueprint = CreateOrderBlueprint().blueprint