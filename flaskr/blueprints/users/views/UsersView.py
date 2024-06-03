from multiprocessing import context
from flaskr.blueprints import *
from ..services.UserService import UserService
from flaskr.blueprints.stores_management.services.StoreService import StoreService

from datetime import datetime

from .EditUserView import edit_user

from .CreateUserView import create_user

users = Blueprint('users', __name__, url_prefix='/users',
                       template_folder='../templates')

# Child blueprint for edit user
users.register_blueprint(edit_user)
users.register_blueprint(create_user)
    
@users.route('/')
def home():
    users = UserService().get_all_active_users()
    
    context = {
        'all_users': users
    }

    return render_template('users.html', context=context)

@users.route('/table')
def users_table():
    users = UserService().get_all()
    
    context = {
        'all_users': users
    }

    return render_template('users_table.html', context=context)