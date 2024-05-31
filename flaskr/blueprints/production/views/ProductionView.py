from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from ..services.ProductionService import ProductionService
from ..services.ProductionChartService import ChartService


production = Blueprint('production', __name__, url_prefix='/production',
                       template_folder='../templates')

@production.route('/')
def home():
    past_days = int(request.args.get('lenght', '0')) or 0
    chart_type = request.args.get('chart_type', 'bar')

    context = {
        'productions' : ProductionService.get_all(),
        'articles' : ProductionService.get_articles(),
        'produced' : ProductionService().get_data_for_total_production(),
        'history' : ProductionService().get_production_history(),
        
        # Chart context
        'chartdata' : ChartService(num_days=past_days).create_chart_datasets(),
        'chartlabels' : ChartService(num_days=past_days).create_labels_for_chart(),
        'type' : str(chart_type)
    }
    return render_template('production.html', context=context)

@production.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    ProductionService().create(data)

    return redirect(url_for('production.home'))

@production.route('/o', methods=['get'])
def o():
    from datetime import datetime
    return f'{ChartService().create_article_data_of_each_day(3)}'

@production.route('/fake/<int:d>', methods=['get'])
def fake(d):
    if d == 1:
        ProductionService().create_random_production(forward=True)
    else:
        ProductionService().create_random_production(days=d)
    
    return 'ok'












