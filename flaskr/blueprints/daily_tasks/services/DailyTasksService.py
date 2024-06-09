from flaskr.blueprints.daily_tasks.models.DailyTaskModel import DailyTaskModel
from flaskr.extensions import db

class DailyTasksService:
    def __init__(self, id=None):
        self.id = id
        
    def get_all_active_tasks(self):
        return db.session.query(DailyTaskModel).filter(
            DailyTaskModel.status == False).all()
    
    def create_task(self, data):
        task = DailyTaskModel(**data)
        db.session.add(task)
        db.session.commit()