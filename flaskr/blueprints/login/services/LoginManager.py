from flaskr.extensions import login_manager
from flaskr.blueprints.users.models.users_model import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must be logged to see that page')
    return redirect('/login')