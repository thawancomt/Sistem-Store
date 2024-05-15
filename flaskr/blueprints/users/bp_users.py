from flaskr.blueprints import *

from flaskr.models.users import User, Session
from flaskr.models.production import Production, Consumes
from flaskr.models.stores_management import Store

from datetime import datetime

from .bp_edit_user import bp_edit_user

users_page_bp = Blueprint('users_page_bp', __name__, url_prefix='/users')

# Child blueprint for edit user
users_page_bp.register_blueprint(bp_edit_user)


def user_data(date_for='', store_to_show=0):

    data = {}

    if not date_for:
        date_for = datetime.now().strftime('%y%m%d')

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
    
@users_page_bp.route('/')
def show_users():

    if is_user_logged_in(external_ip()):
        pass
    else:
        return redirect('/login')

    context = {}

    context['data'] = user_data()
    context['users'] = User().return_all_users()

    return render_template('users/users.html', context=context)
