from flask import Blueprint, request, redirect, flash, render_template, url_for

from flaskr.models.users import User, Session
from flaskr.models.production import Production, Consumes
from flaskr.models.stores_management import Store



from datetime import datetime

home_bp = Blueprint('home_bp', __name__, url_prefix='/homepage')

date = datetime.now().strftime('%Y-%m-%d')


def user_data(date_for='', store_to_show=0):

    data = {}

    if not date_for:
        date_for = date.today()

    if store_to_show:
        data['total_of_the_day'] = Production(date_for).get_already_produced(store_to_show)
        data['store_name'] = Session(external_ip()).store_name()

    data['username'] = Session(external_ip()).name()
    data['level'] = Session(external_ip()).level()
    data['articles'] = Production.articles
    data['stores'] = Production.stores
    return data


def external_ip():
    return request.remote_addr

def is_user_logged_in(ip):
    # Check if user is logged in
    try:
        result = Session.connected_users[ip]['status']
        if result:
            return True
    except KeyError:
        return False



from flaskr.blueprints.tasks.task_service import TaskService
@home_bp.route('/', methods=['GET', 'POST'])
def home():
    if not is_user_logged_in(external_ip()):
        return redirect(url_for('login_bp.login_page'))


    user_store = Session(external_ip()).store_name(id=True)
    
    date_for = datetime.now().strftime('%Y-%m-%d')

    store_to_show = user_store


    # Object to get management of the store
    store = Store()
    store.store = 5

    # Create a context to send to the templates
    context = {
        'store_to_show': store_to_show,
        'data': user_data(date_for, store_to_show),
    }

    context['level'] = context['data']['level']

    # Store context
    context['workers'] = User().return_filtered_users_by_store(int(store_to_show))
    context['store_to_show'] = store_to_show
    context['date_for'] = date_for
    context['stores'] = Production.stores

    # Production context
    context['chart_data'] = Production(date_for).create_data_to_ball_usage_chart(store_to_show, -2)
    context['dates'] = Production(date_for).create_data_to_ball_usage_chart(store_to_show, -7)['labels']

    # Consume context
    context['consumes'] = Consumes().get_consume_by_day(int(store_to_show), date_for)
    context['consume_data'] = Consumes().create_data_to_consume_chart(int(store_to_show), date_for)
    
    # Task context
    context['tasks'] = TaskService().get_tasks()

    # Handle the POST request
    if request.method == 'POST':

        store_to_redirect = request.form.get("store_by_select_form")

        context['store_to_show'] = int(store_to_redirect)

        return redirect(f'/homepage/{date_for}/{store_to_redirect}')

    return render_template('store/homepage.html', context=context, date_for=date_for, store_to_show=store.store)