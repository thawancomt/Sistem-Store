from store.extensions import db, Service
from ..models.ProductionModel import Production
from flask_login import current_user

from ...articles.services.ArticlesService import ArticlesService
from store.blueprints.product_shelf_life.Services.ShelLifeService import ShelLifeService

from sqlalchemy import func, and_
from datetime import datetime, timedelta

from flask import g


from store.blueprints.articles.models.ShelfModel import ShelfLifeModel

class ProductionService(Service):
    def __init__(self, article_id = None, quantity = None, date = None, store_id = None) -> None:
        self.store_id = current_user.store_id or store_id
        self.creator_id = current_user.id
        self.article_id = article_id
        self.quantity = quantity
        self.date : str = date or g.date
        self.articles = self.get_articles()
        
        self.total_production = self.get_data_for_total_production()
        
        self.total_cost = self.get_total_cost(production=self.total_production)
        
        self.all_production_cost = sum(float(x) for x in self.total_cost.values())
        
        self.history = self.get_production_history()
        
    @staticmethod
    def get_articles():
        return ArticlesService.get_all_producibles()
    
    @staticmethod
    def get_all():
        return db.session.query(Production).all()
    
    def create(self, data):
        
        def insert_alert_on_shelf_life(article_id):
            shelf_life = ShelLifeService(article_id=article_id)
            shelf_life.insert()
            
        date = g.date
        
        date = datetime.strptime(date, '%Y-%m-%d') if date else datetime.now()
        
        for article_id, quantity in data.items():
            
            if quantity and int(quantity):
                production = Production(
                    store_id=self.store_id,
                    creator_id=self.creator_id,
                    article_id=article_id,
                    quantity=quantity,
                    date = datetime.now().replace(date.year, date.month, date.day)
                )
                db.session.add(production)
                
                insert_alert_on_shelf_life(article_id)
        
        db.session.commit()


        
    def delete(self, id):
        production = db.session.query(Production).get(id)
        db.session.delete(production)
        db.session.commit()
        
    def delete_all_production_by_article_id(self, article_id):
        all_production = self.get_all()
        
        for production in all_production:
            if production.article_id == int(article_id):
                db.session.delete(production)
        
        db.session.commit()
        
        
    def get_already_prodeced(self) -> Production:
        actual_day = self.date
        next_day = (datetime.strptime(actual_day, '%Y-%m-%d') + timedelta(days=1))
        
        return db.session.query(
            Production.article_id,
            func.sum(Production.quantity).label('quantity')
            ) \
            .filter(and_(Production.store_id == self.store_id, Production.date >= actual_day, Production.date < next_day)) \
            .group_by(Production.article_id).all()
        
        
    def get_data_for_total_production(self) -> dict:
        production = self.get_already_prodeced()

        return dict(production)
    
    def get_production_history(self):
        today = self.date
        tomorrow = (datetime.strptime(today, '%Y-%m-%d') + timedelta(days=1))
        
        return db.session.query(Production).filter(
                and_(
                    Production.store_id == self.store_id,
                    Production.date >= today,
                    Production.date <= tomorrow,
                )
            ).all()
    
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
    
    def get_total_cost(self, production = None):
        
        total_production = production or self.get_data_for_total_production()

        articles = self.get_articles()

        return {
            article.id: f'{(int(total_production.get(article.id, 0)) * article.price):.2f}'
            for article in articles
        }