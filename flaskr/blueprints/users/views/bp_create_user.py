from flaskr.blueprints import *

from ..services.user_service import UserService

create_user = Blueprint('create_user', __name__, url_prefix='/create')

import json

from sqlalchemy.exc import IntegrityError


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
        flash('User already exists')
        return redirect('/')
        
    return redirect('/')

