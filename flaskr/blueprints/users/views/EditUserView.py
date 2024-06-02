from flaskr.blueprints import *
from flaskr.blueprints.users.services.UserService import UserService
from datetime import datetime
from flaskr.blueprints.users.models.UserModel import User
from flaskr.blueprints.stores_management.services.StoreService import StoreService


edit_user = Blueprint('edit_user', __name__)



@edit_user.route('/<username>', methods=['GET'])
def edit_view(username):
    
    user_data = UserService(username = username).get_user_by_username()
    
    
    context = {
        'user' : user_data,
        'stores' : StoreService().get_all_stores()
    }
    
    
    
    
    return render_template('edit_user.html', context=context  )

@edit_user.route('/edit', methods=['POST'])
def update():  # sourcery skip: avoid-builtin-shadow
    data = request.form.to_dict()
    
    username = data['username']
    
    UserService().update(username=username, data=data)
    
    return redirect(url_for('homepage.home'))

@edit_user.route('/delete', methods=['POST'])
def delete():
    """
    Due to the history of production, the delete approach is not possible
    then user will update as an inactive user on database"""
    
    user_id = request.form.get('user_id')
    
    UserService.delete_user_by_id(id=user_id)

    return redirect(url_for('homepage.home'))