from flaskr.blueprints import *
from flaskr.blueprints.stores_management.services.stores_service import StoresService

from ..services.user_service import UserService


create_user = Blueprint('create_user', __name__, url_prefix='/create')

import json

from sqlalchemy.exc import IntegrityError

@create_user.route('/')
def create_user_page():
    context = {
        'stores' : StoresService().get_all()
    }
    return render_template('auth/register.html', context=context)

@create_user.route('/', methods=['POST'])
def create():
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    store = request.form.get('store')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    newUser = UserService()
    
    try:
        newUser.create(username, email, password, store)
        flash('User created successfully')
    except IntegrityError as e:
        flash(f'{e.orig}')
        return redirect('/')
        
    return redirect('/')


