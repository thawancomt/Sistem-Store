from store.blueprints.daily_tasks.models.DailyTaskModel import DailyTaskModel
from store.extensions import db
from datetime import datetime
from flask_login import current_user

from sqlalchemy import and_, or_





class DailyTasksService:
    def __init__(self, id=None, date = None):
        self.id = id
        self.date = date
        self.task : DailyTaskModel = self.get_task_by_id(self.id)
        
    def get_all_active_tasks(self) -> list[DailyTaskModel] | None :
        return db.session.query(DailyTaskModel).filter(
            DailyTaskModel.status == True).all()
    
    def get_all_inactive_tasks(self) -> list[DailyTaskModel] | None:
        return db.session.query(DailyTaskModel).filter(
            or_(DailyTaskModel.status == False,
                DailyTaskModel.end_at)
            ).all()
    
    def get_all_tasks(self) -> list[DailyTaskModel] | None:
        return db.session.query(DailyTaskModel).all()
    

    def get_task_by_id(self, task_id) -> list[DailyTaskModel] | None:
        return db.session.query(DailyTaskModel).get(task_id)


    
    def create_task(self, data) -> None:
        task = DailyTaskModel(**data, created_by=current_user.id)
        db.session.add(task)
        db.session.commit()

    def deactive_task(self, task_id) -> bool:
        if task := db.session.query(DailyTaskModel).get(task_id):
            task.status = False
            task.end_at = self.date or datetime.now()
            task.finished_by = current_user.id
            db.session.commit()
            return True
        return False

    def update_task(self, data : dict) -> None:
        self.task.name = data.get('name') or self.task.name
        self.task.description = data.get('description') or self.task.description
        
        self.task.status = bool(data.get('status'))
        
        self.task.start_at = data.get('start_at') or self.task.start_at
        self.task.end_at = data.get('end_at') or self.task.end_at
        
        self.task.finished_by = data.get('finished_by') or self.task.finished_by
        
        db.session.commit()