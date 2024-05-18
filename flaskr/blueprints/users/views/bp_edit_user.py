from flaskr.blueprints import *
from flaskr.blueprints.users.services.user_service import UserService
from datetime import datetime



bp_edit_user = Blueprint('edit_user', __name__, url_prefix='/edit')



@bp_edit_user.route('/<username>', methods=['GET', 'POST'])
def edit(username ):
    
    user_data = UserService().get_user_by(username=username)
    
    
    context = {
        'username': user_data.username,
        'email' : user_data.email,
        'password' : user_data.password,
    }
    
    
    return render_template('users/edit_user.html', context=context  )

def edit_user(username):
    user_data = UserService().get_user_by(username=username)
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    
    UserService().update()

@bp_edit_user.route('/delete/<username>', methods=['POST'])
def delete(username):
    UserService().delete_user_by_username(username=username)
    flash(f'User {username} has been deleted',)
    return redirect(url_for('home_bp.home'))