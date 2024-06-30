from store.extensions import db

from flask_login import current_user

from ..models.StockModel import Stock

from store.blueprints.articles.models.ArticleModel import ArticleModel

from store.blueprints.articles.services.ArticlesService import ArticlesService

from datetime import datetime, timedelta

from sqlalchemy import func, and_, select

class StockServices:
    def __init__(self, store_id = None,
                 article_id = None,
                 quantity = None,
                 date = None):
        
        self.store_id = store_id or current_user.store_id
        self.article_id = article_id
        self.quantity = quantity
        self.date = date or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.articles = ArticlesService.get_all_stockable()
        self.per_page = 3
        
    def get_all(self):
        return db.session.query(Stock).all()
    
    def get_stock(self):
        return db.session.query(
            Stock.article_id,
            Stock.quantity
        ).filter(
            and_(
                Stock.store_id == self.store_id,
                Stock.date == self.date
                )) \
        .order_by(Stock.date.desc()).all()
        
    def get_stocks_dates(self):
        return db.session.query(
            Stock.date
        ).group_by(Stock.date).order_by(Stock.date.asc()).all()
        
    def convert_stock_object_to_dict(self):
        stock = dict(self.get_stock())
        
        return {
            article.id: stock.get(article.id, 0) for article in self.articles
        } 
    
    def get_data_for_stock_total(self):
        return self.convert_stock_object_to_dict()
    
    def create_stock(self, data : dict):
        self.date = data.get('date')
    
        del data['date']
        
        if stock := db.session.query(Stock).filter(and_(Stock.date == self.date,Stock.store_id == self.store_id)).all():
            self.update_stock(stock=stock, data=data)
            return True
                
        
        for article_id, quantity in data.items():
            if int(quantity) > 0:
                stock = Stock(
                    date = self.date,
                    article_id=article_id,
                    quantity=quantity,
                    store_id = self.store_id,
                    
                    
                )
                db.session.add(stock)
            
        db.session.commit()
        
    
    def update_stock(self, stock = None, data = None):
        if stock := db.session.query(Stock).filter(and_(Stock.date == self.date,Stock.store_id == self.store_id)).all():
            for row in stock:
                row.quantity = int(data.get(f'{row.article_id}', 0)) or row.quantity
            db.session.commit()
            
        return True
    
    def delete_stock(self):
        if stock := db.session.query(Stock).filter(and_(Stock.date == self.date,Stock.store_id == self.store_id)).all():
            for row in stock:
                db.session.delete(row)
            db.session.commit()
            
        return True

    def delete_all_stock_by_article_id(self, article_id):
        stocks = self.get_all()
        
        for stock_ in stocks:
            if stock_.article_id == article_id:
                db.session.delete(stock_)

        db.session.commit()
        
        return True
    
    def create_data_for_stock_table(self):
        stocks = db.session.query(
            Stock.date,
            func.count(Stock.article_id.distinct()).label('count'),
        ).filter(
            and_(Stock.store_id == self.store_id, Stock.date < self.date)
            ).group_by(Stock.date).order_by(Stock.date.desc())

        return stocks.paginate(per_page = 3)
