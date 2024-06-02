from flask import  Blueprint, render_template, request, redirect, url_for, flash

from flask_login import current_user

from ..services.StockServices import StockServices, datetime, ArticlesService

# services


stock = Blueprint('stock', __name__,
                  template_folder='../templates',
                  url_prefix='/stock')

@stock.route('/')
def index():
    context = {
        'title': 'Stock',
        'stock' : StockServices().get_stock(), 
        'articles' : ArticlesService.get_all()
    }
    return render_template('stock.html', context=context)

@stock.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    
    stock = StockServices().create_stock(data=data)
    
    
    return redirect(url_for('stock.index'))