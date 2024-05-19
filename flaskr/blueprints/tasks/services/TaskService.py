from flaskr.blueprints.tasks.models.TaskModel import Task
from flaskr.extensions import db



class TaskService:
    
    def __init__(self, task : str = None, task_description : str = None, task_id : int = None):
        self.db = db
        
        self.taskName = task
        self.taskDescription = task_description
        self.taskId = task_id
        
    def create(self):
        newTask = Task() 
        newTask.name = self.task_name
        newTask.description = self.task_description
        
        self.db.session.add(newTask)
        self.db.session.commit()
    
    def delete(self, id):
        task = Task.query.filter_by(id=id).delete()
        self.db.session.commit()
    
    def get_tasks(self):
        return self.db.session.query(Task).all()