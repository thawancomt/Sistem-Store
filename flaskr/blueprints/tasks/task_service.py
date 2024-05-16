from flaskr.blueprints.tasks.task_model import Task
from flaskr.extensions import db



class TaskService:
    
    def __init__(self):
        self.db = db
        self.db.create_all()
        
    def create(self, name, description):
        newTask = Task()
        newTask.name = name
        newTask.description = description
        
        
        self.db.session.add(newTask)
        self.db.session.commit()
    
    def delete(self, id):
        task = Task.query.filter_by(id=id).delete()
        self.db.session.commit()
        
    def get_task(self, id):
        return self.db.session.query(Task).get(id)
    
    def get_tasks(self):
        return self.db.session.query(Task).all()