from flaskr.blueprints import *
tasks_bp = Blueprint('tasks_bp', __name__,
                     url_prefix='/tasks')


from flaskr.blueprints.tasks.task_service import TaskService


@tasks_bp.route('/create/', methods=['POST'])
def create():
    
    
    name = request.form.get('task_to_send')
    description = request.form.get('task_description')
    
    task_ = TaskService()
    task_.create(name, description)
    
    
    
    return redirect(url_for('home_bp.home'))

@tasks_bp.route('/delete/', methods=['POST'])
def delete():
    
    task_id = request.form.get('task_id')
    
    task_ = TaskService()
    task_.delete(task_id)
    
    return redirect(url_for('home_bp.home'))

def update():
    pass

def get():
    pass

def get_all():
    pass