from flask import g

from store.extensions import db

from store.blueprints.articles.services.ArticlesService import ArticlesService
from store.blueprints.articles.models.ShelfModel import ShelfLifeModel

from datetime import datetime, timedelta

from sqlalchemy import and_, or_



class ShelLifeService():
    def __init__(self, article_id = None):
        self.article_id = article_id
        self.article = self.get_article_by_id()
        
    def get_article_by_id(self):
        return ArticlesService().get_by_id(self.article_id)
    
    def insert(self):
        if self.check_if_is_already_inserted():
            return None
        
        alert = ShelfLifeModel()
        alert.initial_date = g.date
        alert.expiration_date = datetime.strptime(g.date, '%Y-%m-%d') + timedelta(days=self.article.shelf_life)
        alert.article_id = self.article_id
        
        db.session.add(alert)
        db.session.commit()
        
        return alert
    
    def check_if_is_already_inserted(self):
        return db.session.query(ShelfLifeModel).where(and_(ShelfLifeModel.article_id == self.article_id, ShelfLifeModel.expiration_date == g.date)).first()
    
    def get_by_date(self):
        return db.session.query(ShelfLifeModel).where(ShelfLifeModel.expiration_date == g.date).all()