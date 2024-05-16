from flaskr.blueprints import *

from flaskr.models.stores_management import Store




tasks_bp = Blueprint('tasks_bp', __name__,
                     url_prefix='/tasks')


@tasks_bp.route('/create/', methods=['POST'])
def create_task():
    
    from flaskr.blueprints.tasks.task_service import TaskService
    
    name = request.form.get('task_to_send')
    description = request.form.get('task_description')
    
    task_ = TaskService()
    task_.create(name, description)
    
    
    
    return redirect(url_for('home_bp.home'))