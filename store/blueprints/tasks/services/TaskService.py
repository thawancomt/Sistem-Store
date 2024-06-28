from store.blueprints.tasks.models.TaskModel import Task

from flask import g
from store.extensions import db

from datetime import datetime, timedelta


from flask_login import current_user

from sqlalchemy import and_

class TaskService:
    
    def __init__(self, task_name : str = None, task_description : str = None, task_id : int = None, store_id : int = None, user_id : int = None):
        self.task_name = task_name
        self.task_description = task_description
        self.taskId = task_id
        self.store_id = store_id
        self.user_id = user_id
        
    def create(self):
        new_task = Task()  
        new_task.name = self.task_name # 
        new_task.description = self.task_description #
        new_task.created_by = current_user.id or self.user_id #
        
        new_task.created_at = datetime.now()
        new_task.store_id = self.store_id or current_user.store_id 
        
        db.session.add(new_task)
        db.session.commit()
        
    def finish(self):
        if task := db.session.query(Task).filter(Task.id == self.taskId).one_or_none():
            task.finished_by = current_user.id
            task.status = True
            task.finished_at = datetime.now()
            db.session.commit()
            
        else:
            return False
    
    def delete(self, id):
        task = Task.query.filter_by(id=id).delete()
        db.session.commit()
    
    def get_tasks(self):
        return db.session.query(
            Task
        ).filter(
            Task.store_id == current_user.store_id
        ).all()
    
    @staticmethod
    def get_tasks_of_day():
        limit = datetime.strptime(g.date, '%Y-%m-%d')
        return db.session.query(
            Task
        ).filter(
            and_(
                Task.created_at >= limit,
                Task.created_at < (limit + timedelta(days=1)).strftime('%Y-%m-%d')
            )
        ).all()
        
    @staticmethod
    def get_active_tasks_of_day():
        tasks = TaskService.get_tasks_of_day()
        return [task for task in tasks if task.status == False]

    @staticmethod
    def get_done_tasks_of_day():
        tasks = TaskService.get_tasks_of_day()
        return [task for task in tasks if task.status == True]