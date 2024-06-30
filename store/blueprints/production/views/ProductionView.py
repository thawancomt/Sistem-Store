from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g

from ..services.ProductionService import ProductionService, current_user, datetime
from ..services.ProductionChartService import ChartService


production = Blueprint('production', __name__,
                       url_prefix='/production',
                       template_folder='../templates',
                       static_folder='../static')

@production.route('/')
def home():
    store_id = request.args.get('store_id') or current_user.store_id
    date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
    return redirect(url_for('production.homepage', store_id = store_id, date = date))

@production.route('/<store_id>/')
def homepage(store_id):
    
    past_days = int(request.args.get('lenght', '0')) or 30
    chart_type = request.args.get('chart_type', 'bar')

    context = {
        'articles' : ProductionService.get_articles(),
        'produced' : ProductionService(store_id=store_id, date=g.date).get_data_for_total_production(),
        'history' : ProductionService(store_id=store_id, date=g.date).get_production_history(),
        
        # Chart context
        'chartdata' : ChartService(how_many_days=past_days, date=g.date).create_chart_datasets(),
        'chartlabels' : ChartService(how_many_days=past_days, date=g.date).create_date_labels_for_chart(),
        'type' : str(chart_type)
    }
    return render_template('production.html', context=context)

@production.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    data['date'] = g.date
    
    ProductionService().create(data)
    

    return redirect(url_for('production.home'))












