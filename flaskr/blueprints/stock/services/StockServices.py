from flaskr.extensions import db

from flask_login import current_user

from ..models.StockModel import Stock

from flaskr.blueprints.articles.models.ArticleModel import ArticleModel

from flaskr.blueprints.articles.services.ArticlesService import ArticlesService

from datetime import datetime, timedelta

from sqlalchemy import func, and_

class StockServices:
    def __init__(self, store_id = None,
                 article_id = None,
                 quantity = None,
                 date = None):
        
        self.store_id = store_id or current_user.store_id
        self.article_id = article_id
        self.quantity = quantity
        self.date = date or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_stock(self):
        return db.session.query(
            Stock.article_id,
            Stock.quantity
        ).filter(
            and_(
                Stock.store_id == self.store_id,
                Stock.date == self.date
                )) \
        .all()
        
    def get_stocks_dates(self):
        return db.session.query(
            Stock.date
        ).group_by(Stock.date).all()
        
    def convert_stock_object_to_dict(self):
        stock = self.get_stock()
        return dict(stock)
    
    def get_data_for_stock_total(self):
        return self.convert_stock_object_to_dict()
    
    def create_stock(self, data):
        self.date = data.get('date')
    
        del data['date']
        
        for article_id, quantity in data.items():
            stock = Stock(
                date = self.date,
                article_id=article_id,
                quantity=quantity,
                store_id = self.store_id,
                
                
            )
            db.session.add(stock)
            
        db.session.commit()
