from store.utils import *
from store.extensions import BlueprintBase, current_user

from ...articles.services.ArticlesService import ArticlesService
from ...stock.services.StockServices import StockServices
from ...stores_management.services.StoreService import StoreService

from ..services.PDFCreator import PDFCreator
from ..services.OrdersServices import OrderService

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
        self.blueprint.add_url_rule('/orders', 'orders', self.orders, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/download/<int:order_id>', 'download', self.download_pdf_order, methods=['GET'])

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


        pdf.save_db(store_id, pdf.buffer.read(), g.date)

        return send_file(pdf_buffer, as_attachment=True, download_name='order.pdf', mimetype='application/pdf')
        
    def update(self):
        pass
    def delete(self):
        pass
    
    def orders(self):
        orders = OrderService().get_all()
        store = None

        if request.method == 'POST':
            store = request.form.get('store_id', current_user.store_id)
            orders = OrderService(store_id=store).get_by_store()


        context = {
            'orders' : orders,
            'stores' : StoreService().get_all_stores() 
        }

        return render_template('Orders.html', context=context)

    def download_pdf_order(self, order_id):
        import io
        pdf_buffer = OrderService(order_id=order_id).get_by_id()

        pdf_file = io.BytesIO(pdf_buffer.file)

        return send_file(pdf_file, as_attachment=True, download_name='order.pdf', mimetype='application/pdf')

CreateOrderBlueprint = CreateOrderBlueprint().blueprint