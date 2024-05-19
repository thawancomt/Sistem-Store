from flaskr.blueprints import *
from datetime import datetime

homepage = Blueprint('homepage', __name__, url_prefix='/homepage')


from flaskr.blueprints.tasks.services.TaskService import TaskService
from flaskr.blueprints.stores_management.services.StoreService import StoreService
from flask_login import login_required, current_user



@homepage.route('/', methods=['GET', 'POST'])
@login_required
def home():
    
    context = {'tasks': TaskService().get_tasks()}
    context['store_name'] = StoreService().get_by_id(current_user.store).name
    
    
    return render_template('store/homepage.html', context=context)
