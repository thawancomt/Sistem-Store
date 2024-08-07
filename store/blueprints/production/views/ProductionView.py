from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g

from ..services.ProductionService import ProductionService, current_user, datetime
from ..services.ProductionChartService import ProductionChartService

from flask_login import login_required, fresh_login_required


production = Blueprint('production', __name__,
                       url_prefix='/production',
                       template_folder='../templates',
                       static_folder='../static')

@production.route('/')
@login_required
def home():
    store_id = request.args.get('store_id') or current_user.store_id
    date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
    return redirect(url_for('production.homepage', store_id = store_id, date = date))

@production.route('/<store_id>/')
@login_required
def homepage(store_id):
    
    past_days = int(request.args.get('lenght', '0')) or 31
    
    production_chart = ProductionChartService(g.date, past_days, store_id)
    
    production_data = ProductionService(store_id=store_id, date=g.date)

    context = {
        'articles' : production_data.articles,
        'produced' : production_data.total_production,
        'history' : production_data.history,
        'total_production_cost' : production_data.total_cost,
        'sum_total_cost' : production_data.all_production_cost,
        
        # Chart context
        'chartdata' : production_chart.dataset,
        'chartlabels' : production_chart.date_labels
    }


    return render_template('production.html', context=context)

@production.route('/create', methods=['POST'])
@login_required
def create():
    data = request.form.to_dict()
    ProductionService().create(data)
    

    return redirect(url_for('production.home', date=g.date))




# A fake production to chart

@production.route('/chart')
@login_required
def chart():
    ProductionService().create_random_production()
    return redirect('/homepage')

