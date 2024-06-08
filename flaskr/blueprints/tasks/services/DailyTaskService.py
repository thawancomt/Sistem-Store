from flaskr.extensions import db

from flask_login import current_user

from ..models.DailyTaskModel import DailyTaskModel
from ..models.DailyTaskStatusModel import DailyTaskStatusModel

from sqlalchemy import func, and_
#Python buildin
from datetime import datetime


class DailyTaskService:
    def __init__(self, store_id = None, task_id = None, name = None, description = None, user_id = None):
        self.store_id = store_id or current_user.store_id
        self.id = task_id
        self.name = name
        self.description = description
        self.creator = user_id or current_user.id
        
    @staticmethod
    def get_all():
        return db.session.query(DailyTaskModel).filter(DailyTaskModel.active == True).all()
    
    def create(self):
        new_task = DailyTaskModel(
            name = self.name,
            description = self.description,
            store_id = self.store_id,
            creator = self.creator,
            start_date = datetime.now().strftime('%Y-%m-%d')
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task



class DailyTaskStatusService():
    def __init__(self, date = None):
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        self.initialize_day()
        self.tasks = self.get_all()
    
        
    
    def initialize_day(self):
        tasks_created = [str(task.task_id) for task in db.session.query(DailyTaskStatusModel.task_id).filter(
            DailyTaskStatusModel.date == self.date
        ).all()]

        active_tasks = DailyTaskService.get_all()
        
        for task in active_tasks:
            if str(task.id) not in tasks_created and task.store_id == current_user.store_id and task.start_date <= datetime.strptime(self.date, '%Y-%m-%d'):
                task_status = DailyTaskStatusModel(
                    task_id = task.id,
                    date = self.date
                )
                db.session.add(task_status)
        db.session.commit()
        
       
    def get_all(self):
        all_tasks_status = db.session.query(
            DailyTaskStatusModel
        ).filter(
            DailyTaskStatusModel.date == self.date
        ).all()
        
        return all_tasks_status
    
    def get_by_task_id(self, task_id):
        return db.session.query(
            DailyTaskStatusModel).filter(
                and_(
                    DailyTaskStatusModel.date == self.date, 
                    DailyTaskStatusModel.task_id == task_id
                )
            ).first()
    
        
    def set_as_done(self, data):
        for task in self.tasks:
            if str(task.task_id) in data:
                task.status = True
            else:
                task.status = False
        db.session.commit()
        

        
    


