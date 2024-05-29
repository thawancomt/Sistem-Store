from flaskr.blueprints.tasks.models.TaskModel import Task
from flaskr.extensions import db

from flask_login import current_user

class TaskService:
    
    def __init__(self, task_name : str = None, task_description : str = None, task_id : int = None):
        self.task_name = task_name
        self.task_description = task_description
        self.taskId = task_id
        
    def create(self):
        new_task = Task() 
        new_task.name = self.task_name
        new_task.description = self.task_description
        new_task.created_by = current_user.id
        new_task.finished_by = None
        new_task.status = 'On going'
        
        db.session.add(new_task)
        db.session.commit()
        
    def finish(self):
        if task := db.session.query(Task).filter(Task.id == self.taskId).one_or_none():
            task.finished_by = current_user.id
            task.status = 'finished'
            db.session.commit()
            
        else:
            return False
    
    def delete(self, id):
        task = Task.query.filter_by(id=id).delete()
        db.session.commit()
    
    def get_tasks(self):
        return db.session.query(Task).all()