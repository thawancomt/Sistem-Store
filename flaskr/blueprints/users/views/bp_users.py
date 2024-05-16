from multiprocessing import context
from flaskr.blueprints import *
from flaskr.blueprints.users.services.user_service import UserService

from datetime import datetime

from .bp_edit_user import bp_edit_user

from .bp_create_user import create_user

users_page_bp = Blueprint('users_page_bp', __name__, url_prefix='/users')

# Child blueprint for edit user
users_page_bp.register_blueprint(bp_edit_user)
users_page_bp.register_blueprint(create_user)
    
@users_page_bp.route('/')
def show_users():
    users = UserService().get_all()
    
    context = {
        'all_users': users
    }

    return render_template('users/users.html', context=context)
