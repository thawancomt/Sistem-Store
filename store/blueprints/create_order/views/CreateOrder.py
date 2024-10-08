from store.utils import *
from store.extensions import BlueprintBase, current_user, login_required

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
        self.blueprint.add_url_rule('/accept_order', 'accept_order', self.accept_order, methods=['GET', 'POST'])

    def index(self):

        store_id = request.args.get('store_id') or current_user.store_id

        if stock_dates := StockServices(store_id=store_id).get_stocks_dates():
            last_stock = StockServices(store_id=store_id, date=stock_dates[-1].date).get_stock()

            if len(stock_dates) > 1:
                before_last_stock = StockServices(store_id=store_id,date=stock_dates[-2].date).get_stock()

            else:
                before_last_stock = []
        
        else:
            last_stock = []
            before_last_stock = []
            
        context = {
            'articles' : ArticlesService().get_all_active(),
            'last_stock' : StockServices().convert_stock_object_to_dict(last_stock),
            'before_last_stock' : StockServices().convert_stock_object_to_dict(before_last_stock),
            'dates' : stock_dates,
            'stores' : StoreService().get_all_stores(),
            'active_store' : StoreService().get_by_id(store_id).name
        }
        return render_template('index.html', **context)
    
    @login_required
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

        order = OrderService(store_id=store_id)
        order = order.save_db(store=store_id, file=bytes(), data=data)
        
        pdf = PDFCreator(order = order)       
        pdf.draw_header()        
        pdf.draw_items(data=data)
        pdf.pdf.showOutline()    
        pdf_buffer = pdf.create()

        pdf_buffer.seek(0)
        

        pdf_content = pdf_buffer.read()

        pdf_buffer.seek(0)

        OrderService().save_pdf_into_order(order.id, pdf_content)

        filename = f'{order.store.name}_{datetime.strftime(order.create_at, '%Y-%m-%d')}_{order.id}.pdf'

        return send_file(pdf_buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')
        
    def update(self):
        pass
    def delete(self):
        pass

    @login_required
    def orders(self):
        user_store = current_user.store_id

        if not current_user.level:
            orders = OrderService().get_all()
        else:
            orders = OrderService(store_id=user_store).get_by_store()


        if request.method == 'POST':
            selected_store = request.form.get('store_id', current_user.store_id)
            orders = OrderService(store_id=selected_store).get_by_store()


        context = {
            'orders' : orders,
            'stores' : StoreService().get_all_stores() 
        }

        return render_template('Orders.html', **context)
    
    @login_required
    def download_pdf_order(self, order_id):
        import io
        pdf_buffer = OrderService(order_id=order_id).get_by_id()

        pdf_file = io.BytesIO(pdf_buffer.file)

        return send_file(pdf_file, as_attachment=True, download_name='order.pdf', mimetype='application/pdf')
    @login_required   
    def accept_order(self):

        context = {
            'orders' : OrderService().get_all(),
            'eval' : eval
        }

        if request.method == 'POST':
            order_id = request.form.get('order_id')
            OrderService().accept_order(order_id = order_id)

        return render_template('ReviewOrders.html', **context)

CreateOrderBlueprint = CreateOrderBlueprint().blueprint

