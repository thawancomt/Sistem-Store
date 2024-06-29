from store.extensions import db

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
        self.all_daily_tasks : list[datetime]= DailyTasksService().get_all_tasks()
        self.active_tasks = DailyTasksService().get_all_active_tasks()
        self.all_inative_tasks = DailyTasksService().get_all_inactive_tasks()
        
        print(self.all_inative_tasks)
        self.insert_active_task()
        self.all_tasks = self.get_all_tasks()
        self.verify_if_exist_inative_tasks()
        
    def verify_if_task_exist_on_day(self, task_id):
        return db.session.query(
            DailyStatusModel
        ).filter(
            and_(
                DailyStatusModel.date == self.date, 
                DailyStatusModel.task_id == task_id,
            )
        ).first() is not None
    
    def verify_if_exist_inative_tasks(self) -> None:
        for task in self.all_inative_tasks:
            task.end_at = task.end_at or self.date
            if task_ := db.session.query(DailyStatusModel).filter(
                and_(
                    DailyStatusModel.task_id == task.id,
                    DailyStatusModel.date == self.date,
                )
                
            ).first():
                if task.end_at < self.date:
                    db.session.delete(task_)
        
        db.session.commit()
        
        
    def insert_active_task(self):
        
        for task in self.all_daily_tasks:
            task_start_at_formated = datetime(task.start_at.year, task.start_at.month, task.start_at.day)
            end_at = task.end_at or self.date
            if self.verify_if_task_exist_on_day(task.id):
                pass
            elif self.date >= task_start_at_formated and self.date <= end_at: # and self.date <= task.end_at if task.end_at else self.date :
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

        task.status = not undone
        db.session.commit()
        
    def update_day_status(self, data):
        for task in self.all_daily_tasks:
            if str(task.id) in data:
                self.set_as_done(task.id)
            else:
                self.set_as_done(task.id, undone = True)
        