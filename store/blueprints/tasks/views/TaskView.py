
from store.extensions import *
from store.utils import *

from ..services.TaskService import TaskService

class TaskView(BlueprintBase):
    def __init__(self, name=None, static_folder=None, url_prefix=None, template_folder=None, import_name=None,) -> None:
        super().__init__(name, static_folder, url_prefix, template_folder, import_name)
        self.register_routes()

    def register_routes(self):
        self.blueprint.add_url_rule('/task', 'create', self.create, methods=['POST'])
        self.blueprint.add_url_rule('/delete/', 'delete', self.delete, methods=['POST'])
        self.blueprint.add_url_rule('/finish', 'finish', self.finish, methods=['POST'])
        
    def create(self):
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        
        task = TaskService(task_name=task_name, task_description=task_description)
        
        task.create()
        return redirect(url_for('homepage.index'))
    def delete(self):
        task_id = request.form.get('task_id')
    
        task_ = TaskService()
        task_.delete(task_id)
        
        return redirect(url_for('homepage.index', date=g.date))
    
    def finish(self):
        taskID = request.form.get('task_id')
        task = TaskService(task_id=taskID)
        
        if task.finish():
            flash('Task finished')

        return redirect(url_for('homepage.index', date=g.date))
    
    def update(self):
        pass

    def index(self):
        pass

TaskView = TaskView('tasks', url_prefix='/tasks', import_name=__name__).blueprint