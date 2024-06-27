from flaskr.blueprints import *
from flaskr.blueprints.stores_management.services.StoreService import StoreService

from ..services.UserService import UserService

from datetime import datetime


create_user = Blueprint('create_user', __name__, url_prefix='/create',
                        template_folder='../templates',
                        static_folder='../static')

import json

from sqlalchemy.exc import IntegrityError

@create_user.route('/')
def create_user_page():
    context = {
        'stores' : StoreService().get_all_stores()
    }
    return render_template('register.html', context=context)

@create_user.route('/', methods=['POST'])
def create():
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    store = request.form.get('store')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        newUser = UserService(
            username=username,
            email=email, 
            password=password,
            store_id=store,
            created_at=created_at,
            last_login=last_login
        )
        newUser.create()
        flash('User created successfully')
    except IntegrityError as e:
        flash(f'{e.orig}')
        return redirect('/')
    except ValueError:
        flash('You forget na username')
        return redirect(url_for('auth.login_page'))
        
    return redirect('/')


