from flaskr.extensions import db

from flask_login import current_user

from ..models.DailyTaskModel import DailyTaskModel

class DailyTaskService:
    def __init__(self, store_id = None, task_id = None, name = None, description = None, user_id = None):
        self.store_id = store_id or current_user.store_id
        self.id = task_id
        self.name = name
        self.description = description
        self.creator = user_id or current_user.id
        
    @staticmethod
    def get_all():
        return db.session.query(DailyTaskModel).all()
    
    def create(self):
        new_task = DailyTaskModel(
            name = self.name,
            description = self.description,
            store_id = self.store_id,
            creator = self.creator
        )
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return False
        pass