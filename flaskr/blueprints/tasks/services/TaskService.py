from flaskr.blueprints.tasks.models.TaskModel import Task
from flaskr.extensions import db

from flask_login import current_user

class TaskService:
    
    def __init__(self, task_name : str = None, task_description : str = None, task_id : int = None):
        self.db = db
        
        self.task_name = task_name
        self.task_description = task_description
        self.taskId = task_id
        
    def create(self):
        newTask = Task() 
        newTask.name = self.task_name
        newTask.description = self.task_description
        newTask.created_by = current_user.id
        newTask.finished_by = None
        newTask.status = 'On going'
        
        self.db.session.add(newTask)
        self.db.session.commit()
        
    def finish(self):
        if task := db.session.query(Task).filter(Task.id == self.taskId).one_or_none():
            return task
            task.finished_by = current_user.id
            task.status = 'Finished'
            db.session.commit()
            
        else:
            return False
    
    def delete(self, id):
        task = Task.query.filter_by(id=id).delete()
        self.db.session.commit()
    
    def get_tasks(self):
        return self.db.session.query(Task).all()