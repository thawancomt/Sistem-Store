from multiprocessing import context
from store.blueprints import *
from ..services.UserService import UserService
from store.blueprints.stores_management.services.StoreService import StoreService

from datetime import datetime

from .EditUserView import edit_user

from .CreateUserView import create_user

from flask_login import login_required



users = Blueprint('users', __name__, url_prefix='/users',
                       template_folder='../templates',
                       static_folder='../static')

# Child blueprint for edit user
users.register_blueprint(edit_user)
users.register_blueprint(create_user)
    
@users.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_query = request.form.get('user_query', None)
    
    context = {
        'all_users': UserService.get_all_active_users(query=user_query),
        'inactive_users': UserService.get_all_inactive_users(query=user_query)
    }

    return render_template('users.html', context=context)

@users.route('/table')
def users_table():
    users = UserService().get_all()
    
    context = {
        'all_users': users
    }

    return render_template('users_table.html', context=context)
