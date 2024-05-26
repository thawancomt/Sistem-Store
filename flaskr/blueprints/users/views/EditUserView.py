from flaskr.blueprints import *
from flaskr.blueprints.users.services.UserService import UserService
from datetime import datetime
from flaskr.blueprints.users.models.UserModel import User


edit_user = Blueprint('edit_user', __name__, url_prefix='/edit')



@edit_user.route('/<username>', methods=['GET', 'POST'])
def edit(username ):
    
    user_data = UserService().get_user_by(username=username)
    
    
    context = {
        'username': user_data.username,
        'email' : user_data.email,
        'password' : user_data.password,
    }
    
    
    
    
    return render_template('edit_user.html', context=context  )

@edit_user.route('/edit', methods=['POST'])
def update():
    username = request.form.get('old_username')
    user_data = UserService().get_user_by(username=username)
    
    new_username = request.form.get('username')
    new_email = request.form.get('email')   
    return redirect(url_for('homepage.home'))



@edit_user.route('/delete/<username>', methods=['POST'])
def delete(username):
    UserService().delete_user_by_username(username=username)
    flash(f'User {username} has been deleted',)
    return redirect(url_for('home_bp.home'))