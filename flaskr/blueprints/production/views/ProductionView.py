from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..services.ProductionService import ProductionService
from ...articles.services.ArticlesService import ArticlesService

production = Blueprint('production', __name__, url_prefix='/production',
                       template_folder='../templates')

@production.route('/')
def home():
    context = {
        'productions' : ProductionService.get_all(),
        'articles' : ArticlesService.get_all(),
        'produced' : ProductionService().get_data_for_total_production(),
        'history' : ProductionService().get_production_history()
    }
    return render_template('production.html', context=context)

@production.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    ProductionService().create(data)
    
    
    
    
    return redirect(url_for('production.home'))




