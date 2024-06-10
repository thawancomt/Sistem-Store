from flaskr.extensions import db

# SqlAlchemy
from sqlalchemy import func, and_

# Services externs
from .DailyTasksService import DailyTasksService
from ..models.DailyStatusModel import DailyStatusModel

#Python buildin
from datetime import datetime
import json

class DailyStatusService:
    def __init__(self, date = None):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.active_tasks = DailyTasksService().get_all_active_tasks()
        self.insert_active_task()
        
    def verify_if_task_exist_on_day(self, task_id):
        return db.session.query(
            DailyStatusModel
        ).filter(
            and_(
                DailyStatusModel.date == self.date, 
                DailyStatusModel.task_id == task_id,
            )
        ).first() is not None
        
    def insert_active_task(self):
        for task in self.active_tasks:
              print('testando ')
              if self.verify_if_task_exist_on_day(task.id):
                  pass
              else:
                  daily_task = DailyStatusModel(
                      date = self.date,
                      task_id = task.id
                  )
                  db.session.add(daily_task)
        db.session.commit()
        
    def get_all_tasks(self):
        all_tasks = db.session.query(
            DailyStatusModel
        ).filter(
            DailyStatusModel.date == self.date
        ).all()
        
        return all_tasks
    
    def set_as_done(self, task_id, undone = False):
        task = db.session.query(
            DailyStatusModel
        ).filter(
            and_(
                DailyStatusModel.date == self.date,
                DailyStatusModel.task_id == task_id
            )
        ).first()
        
        task.status = False if undone else True
        db.session.commit()
        
    def update_day_status(self, data):
        for task in self.active_tasks:
            if str(task.id) in data:
                self.set_as_done(task.id)
            else:
                self.set_as_done(task.id, undone = True)
        