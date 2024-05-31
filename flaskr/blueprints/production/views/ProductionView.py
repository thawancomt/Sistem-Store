from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from ..services.ProductionService import ProductionService
from ..services.ProductionChartService import ChartService


production = Blueprint('production', __name__, url_prefix='/production',
                       template_folder='../templates')

@production.route('/')
def home():
    context = {
        'productions' : ProductionService.get_all(),
        'articles' : ProductionService.get_articles(),
        'produced' : ProductionService().get_data_for_total_production(),
        'history' : ProductionService().get_production_history(),
        
        # Chart context
        'chartdata' : ChartService().create_chart_datasets(),
        'chartlabels' : ChartService().create_labels_for_chart()
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












