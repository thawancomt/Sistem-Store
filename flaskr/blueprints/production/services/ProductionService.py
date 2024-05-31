from flaskr.extensions import db
from ..models.ProductionModel import Production
from flask_login import current_user

from ...articles.services.ArticlesService import ArticlesService

from sqlalchemy import func, and_
from datetime import datetime, timedelta



class ProductionService:
    def __init__(self, article_id = None, quantity = None, date = None, store_id = None) -> None:
        self.store_id = current_user.store_id or store_id
        self.creator_id = current_user.id
        self.article_id = article_id
        self.quantity = quantity
        self.date = date
    
    @staticmethod
    def get_all():
        return db.session.query(Production).all()
    
    def create(self, data):
        date = data.get('date')
    
        del data['date']
        
        for article_id, quantity in data.items():
            if int(quantity) != 0:
                production = Production(
                    store_id=self.store_id,
                    creator_id=self.creator_id,
                    article_id=article_id,
                    quantity=quantity,
                    date = date
                )
                db.session.add(production)
        
        db.session.commit()
        
        
    def get_already_prodeced(self, day : datetime = None) -> Production:
        day = day or datetime.now()

        next_day = (day + timedelta(days=1))
        
        next_day = next_day.strftime('%Y-%m-%d')
        day = day.strftime('%Y-%m-%d')
        
        return db.session.query(
            Production.article_id,
            func.sum(Production.quantity).label('quantity')
            ) \
            .filter(and_(Production.store_id == self.store_id, Production.date >= day, Production.date <= next_day)) \
            .group_by(Production.article_id).all()
        
    def get_article_by_date(self, date : datetime = None) -> dict:
        self.get_already_prodeced(day = date)
        
        
    def get_data_for_total_production(self) -> dict:
        production = self.get_already_prodeced()

        return dict(production)
    
    def get_production_history(self):
        today = datetime.now().strftime('%Y-%m-%d')
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        return (
            db.session.query(Production)
            .filter(
                and_(
                    Production.store_id == self.store_id,
                    Production.date >= today,
                    Production.date <= tomorrow,
                )
            )
            .all()
        )
    @staticmethod
    def get_articles():
        return ArticlesService.get_all_producibles()
    
    def create_random_production(self, forward = False, days = 30):
        import random
        days = [datetime.now() + timedelta(days=x) for x in range(days)] if forward else [datetime.now() - timedelta(days=x) for x in range(days)]


        articles = {article.id : article.name for article in ArticlesService.get_all_producibles()}

        for day in days:
            for article_id in articles:
                new_production =  Production(
                    store_id = self.store_id,
                    creator_id = self.creator_id,
                    article_id = article_id,
                    quantity = random.randint(3, 44),
                    date = day

                )
                db.session.add(new_production)
        
        db.session.commit()