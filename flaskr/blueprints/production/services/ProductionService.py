from flaskr.extensions import db
from ..models.ProductionModel import Production
from flask_login import current_user


class ProductionService:
    def __init__(self, article_id, quantity, date) -> None:
        self.store_id = current_user.store_id
        self.creator_id = current_user.id
        self.article_id = article_id
        self.quantity = quantity
        self.date = date
    
    @staticmethod
    def get_all():
        return db.session.query(Production).all()
    
    
    def create(self):
        production = Production(store_id=self.store_id, article_id=self.article_id, quantity=self.quantity, date=self.date, creator_id=self.creator_id)
        db.session.add(production)
        db.session.commit()
        