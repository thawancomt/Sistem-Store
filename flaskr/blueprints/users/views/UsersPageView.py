from multiprocessing import context
from flaskr.blueprints import *
from ..services.UserService import UserService

from datetime import datetime

from .EditUserView import edit_user

from .CreateUserView import create_user

users_page = Blueprint('users_page', __name__, url_prefix='/users')

# Child blueprint for edit user
users_page.register_blueprint(edit_user)
users_page.register_blueprint(create_user)
    
@users_page.route('/')
def show_users():
    users = UserService().get_all()
    
    context = {
        'all_users': users
    }

    return render_template('users/users.html', context=context)
