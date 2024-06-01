from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from ..services.ProductionService import ProductionService, current_user, datetime
from ..services.ProductionChartService import ChartService


production = Blueprint('production', __name__, url_prefix='/production',
                       template_folder='../templates')

@production.route('/')
def home():
    store_id = request.args.get('store_id') or current_user.store_id
    date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
    return redirect(url_for('production.homepage', store_id = store_id, date = date))

@production.route('/<store_id>/<date>')
def homepage(store_id, date):

    
    past_days = int(request.args.get('lenght', '0')) or 0
    chart_type = request.args.get('chart_type', 'bar')

    context = {
        'productions' : ProductionService.get_all(),
        'articles' : ProductionService.get_articles(),
        'produced' : ProductionService(store_id=store_id, date=date).get_data_for_total_production(),
        'history' : ProductionService(store_id=store_id, date=date).get_production_history(),
        
        # Chart context
        'chartdata' : ChartService(how_many_days=past_days, date=date).create_chart_datasets(),
        'chartlabels' : ChartService(how_many_days=past_days, date=date).create_date_labels_for_chart(),
        'type' : str(chart_type)
    }
    return render_template('production.html', context=context)

@production.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()

    ProductionService(date=data['date']).create(data)
    
    return redirect(url_for('production.home'))

#@production.route('/o', methods=['get'])
#def o():
#    from datetime import datetime
#    return f'{ChartService().create_article_data_of_each_day(3)}'
#
#@production.route('/fake/<int:d>', methods=['get'])
#def fake(d):
#    if d == 1:
#        ProductionService().create_random_production(forward=True)
#    else:
#        ProductionService().create_random_production(days=d)
#    
#    return 'ok'












