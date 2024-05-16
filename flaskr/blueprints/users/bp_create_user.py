from flaskr.blueprints import *

from .user_service import UserService

create_user = Blueprint('create_user', __name__, url_prefix='/create')


@create_user.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    
    newUser = UserService()
    
    newUser.create(username, email, password)
    
    return redirect('/')