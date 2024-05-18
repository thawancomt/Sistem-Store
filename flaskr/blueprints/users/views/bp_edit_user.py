from flaskr.blueprints import *
from flaskr.blueprints.users.services.user_service import UserService
from datetime import datetime
from flaskr.blueprints.users.models.users_model import User


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

@bp_edit_user.route('/edit', methods=['POST'])
def edit_user():
    username = request.form.get('old_username')
    user_data = UserService().get_user_by(username=username)
    
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    
    old_user = User().query.filter_by(username=username)
    
    UserService().update(old_user, new_username, new_email)
    return redirect(url_for('home_bp.home'))



@bp_edit_user.route('/delete/<username>', methods=['POST'])
def delete(username):
    UserService().delete_user_by_username(username=username)
    flash(f'User {username} has been deleted',)
    return redirect(url_for('home_bp.home'))