from flaskr.blueprints import *
from flaskr.blueprints.users.services.UserService import UserService
from datetime import datetime
from flaskr.blueprints.users.models.UserModel import User
from flaskr.blueprints.stores_management.services.StoreService import StoreService


edit_user = Blueprint('edit_user', __name__, url_prefix='/edit')



@edit_user.route('/<username>', methods=['GET'])
def edit(username ):
    
    user_data = UserService().get_user_by(username=username)
    
    
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

@edit_user.route('/delete/<username>', methods=['POST'])
def delete(username):
    UserService().delete_user_by_username(username=username)
    flash(f'User {username} has been deleted',)
    return redirect(url_for('homepage.home'))