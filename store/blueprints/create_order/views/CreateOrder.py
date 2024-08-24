from store.utils import *
from store.extensions import BlueprintBase

from ...articles.services.ArticlesService import ArticlesService
from ...stock.services.StockServices import StockServices
from ...stores_management.services.StoreService import StoreService

from ..services.PDFCreator import PDFCreator

import math


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
        self.blueprint.add_url_rule('/create', 'create', self.create, methods=['POST'])

    def index(self):
        stock_dates = StockServices().get_stocks_dates()

        last_stock, before_last_stock = StockServices(date=stock_dates[-1].date).get_stock(), StockServices(date=stock_dates[-2].date).get_stock()

        context = {
            'articles' : ArticlesService().get_all_active(),
            'last_stock' : StockServices().convert_stock_object_to_dict(last_stock),
            'before_last_stock' : StockServices().convert_stock_object_to_dict(before_last_stock),
            'dates' : stock_dates,
            'stores' : StoreService().get_all_stores()
        }
        return render_template('index.html', context = context)
    
    def create(self):
        store_id = request.form.get('store_id')

        data = []

        for article, quantity in request.form.items():
            try:
                article =  ArticlesService().get_by_id(int(article))
                data.append(
                    [
                        article.name, quantity, article.provider.name, article.type.name, math.ceil(float(article.price) * int(quantity))
                    ]
                )
            except:
                pass

        pdf = PDFCreator()
        pdf.draw_header()
        pdf.draw_items(data=data)
        pdf.pdf.showOutline()
        pdf_buffer = pdf.create()
        





        return send_file(pdf_buffer, as_attachment=True, download_name='order.pdf', mimetype='application/pdf')
        
    def update(self):
        pass
    def delete(self):
        pass

CreateOrderBlueprint = CreateOrderBlueprint().blueprint