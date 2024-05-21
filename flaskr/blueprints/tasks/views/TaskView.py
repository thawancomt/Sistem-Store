from flaskr.blueprints import *
from flaskr.blueprints.tasks.services.TaskService import TaskService


tasks = Blueprint('tasks', __name__,
                     url_prefix='/tasks')




@tasks.route('/create', methods=['POST'])
def create():
    
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')
    
    task = TaskService(task_name=task_name, task_description=task_description)
    
    task.create()
    
    
    
    return redirect(url_for('homepage.home'))

@tasks.route('/delete/', methods=['POST'])
def delete():
    
    task_id = request.form.get('task_id')
    
    task_ = TaskService()
    task_.delete(task_id)
    
    return redirect(url_for('homepage.home'))
