from flaskr.blueprints import *
from datetime import datetime

home_bp = Blueprint('home_bp', __name__, url_prefix='/homepage')


from flaskr.blueprints.tasks.task_service import TaskService
from flaskr.blueprints.stores_management.services.stores_service import StoresService
from flask_login import login_required


@home_bp.route('/', methods=['GET', 'POST'])
@login_required
def home():


    user_store =5

    date_for = datetime.now().strftime('%Y-%m-%d')

    store_to_show = 5
    context = {'tasks': TaskService().get_tasks()}
    context['store_name'] = StoresService().get_by_id(5).name
    
    
    return render_template('store/homepage.html', context=context, date_for=date_for)
