from flaskr.extensions import db
from flask_login import current_user

from ..models.ProductionModel import Production
from datetime import datetime

class ProductionService:
    def __init__(self, store = None, item = None, amount = None) -> None:
        self.store = store or current_user.store
        self.item = item
        self.amount = amount
        self.date = datetime.now().strftime('%Y-%m-%d')
        self.release_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.new_production = Production(store=self.store,
                   item=self.item,
                   amount=self.amount,
                   date=self.date,
                   release_at=self.release_at)
    
    def get(self):
        return Production.query.filter_by(store=self.store, date=self.date)
    
    def send(self):
        db.session.add(self.new_production)
        db.session.commit()
    
    def update(self):
        Production.query.filter_by(store=self.store, date=self.date).update({
            'amount': int(self.amount) + int(self.get().first().amount)
        })
        db.session.commit()