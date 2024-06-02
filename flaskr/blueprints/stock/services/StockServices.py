from flaskr.extensions import db

from flask_login import current_user

from ..models.StockModel import Stock

from flaskr.blueprints.articles.models.ArticleModel import ArticleModel

from flaskr.blueprints.articles.services.ArticlesService import ArticlesService

from datetime import datetime

class StockServices:
    def __init__(self, store_id = None,
                 article_id = None,
                 quantity = None,
                 date = None):
        
        self.store_id = store_id or current_user.store_id
        self.article_id = article_id
        self.quantity = quantity
        self.date = date
    
    def get_stock(self):
        return db.session.query(Stock).filter_by(store_id = self.store_id).all()

    
    def create_stock(self, data):
        self.date = data.get('date')
    
        del data['date']
        
        for article_id, quantity in data.items():
            if int(quantity) != 0:
                stock = Stock(
                    date = self.date,
                    article_id=article_id,
                    quantity=quantity,
                    store_id = self.store_id,
                    
                    
                )
                db.session.add(stock)
            
        db.session.commit()
