from store.blueprints import *
from store.blueprints.tasks.services.TaskService import TaskService

from flask import g

from flask_login import login_required



tasks = Blueprint('tasks', __name__,
                     url_prefix='/tasks')



@tasks.route('/create', methods=['POST'])
@login_required
def create():
    
    task_name = request.form.get('task_name')
    task_description = request.form.get('task_description')
    
    task = TaskService(task_name=task_name, task_description=task_description)
    
    task.create()
    return redirect(url_for('homepage.index'))

@tasks.route('/delete/', methods=['POST'])
def delete():
    
    task_id = request.form.get('task_id')
    
    task_ = TaskService()
    task_.delete(task_id)
    
    return redirect(url_for('homepage.index', date=g.date))


@tasks.route('/finish', methods=['POST'])
def finish():
    taskID = request.form.get('task_id')
    task = TaskService(task_id=taskID)
    
    if task.finish():
        flash('Task finished')
        
    return redirect(url_for('homepage.index', date=g.date))



