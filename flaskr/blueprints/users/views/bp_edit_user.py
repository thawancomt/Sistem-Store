from flaskr.blueprints import *
from flaskr.blueprints.users.services.user_service import UserService
from datetime import datetime



bp_edit_user = Blueprint('edit_user', __name__, url_prefix='/edit')



@bp_edit_user.route('/<username>', methods=['GET', 'POST'])
def edit(username):
    

    # set old user
    oldUser = UserService().get_user_by(username=username)
    
    if oldUser:
        oldUser = {key:value
                for key, value in oldUser.__dict__.items() if key not in ['_sa_instance_state']}
    

    return f'{str(oldUser)}'