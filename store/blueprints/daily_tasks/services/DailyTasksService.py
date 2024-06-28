from store.blueprints.daily_tasks.models.DailyTaskModel import DailyTaskModel
from store.extensions import db
from datetime import datetime
from flask_login import current_user



class DailyTasksService:
    def __init__(self, id=None, date = None):
        self.id = id
        self.date = date
        
    def get_all_active_tasks(self):
        return db.session.query(DailyTaskModel).filter(
            DailyTaskModel.status == True).all()
    
    def get_all_inactive_tasks(self):
        return db.session.query(DailyTaskModel).filter(
            DailyTaskModel.status == False).all()
    
    def get_all_tasks(self):
        return db.session.query(DailyTaskModel).all()


    
    def create_task(self, data):
        task = DailyTaskModel(**data)
        db.session.add(task)
        db.session.commit()

    def deactive_task(self, task_id):
        if task := db.session.query(DailyTaskModel).get(task_id):
            task.status = False
            task.end_at = self.date or datetime.now()
            task.finished_by = current_user.id
            db.session.commit()
            return True
        return False
    