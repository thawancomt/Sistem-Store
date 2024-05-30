from .ProductionService import ProductionService
from flaskr.extensions import db
from ..models.ProductionModel import Production

from flaskr.blueprints.articles.services.ArticlesService import ArticlesService

from flask_login import current_user

from sqlalchemy import and_
from datetime import datetime, timedelta

import json



class ChartService():
    def __init__(self, store_id = None, num_days=7):
        self.num_days = num_days
        self.store_id = store_id or current_user.store_id
        self.date_labels = self.create_labels()
        self.articles = ArticlesService.get_all()
        
        self.production = self.create_dataset()
        
        
    



    def create_labels(self) -> list:
        
        label = [datetime.now().strftime('%Y-%m-%d')]
        
        label += [
            (datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range(1, self.num_days + 1)
            ]
        
        return label
    

    def get_articles(self):
        return [article.name for article in self.articles]
    
    def create_data(self, day=None):
        production = ProductionService().get_already_prodeced(day=day)

        production_dict = { production.article_id: int(production.quantity) for production in production }

        return {
            article.id: production_dict.get(article.id, 0)
            for article in self.articles
        }
        
    def create_dataset(self):
        a = {}
        for day in self.date_labels:
            day = datetime.strptime(day, '%Y-%m-%d')
            a[datetime.strftime(day, '%Y-%m-%d')] = (self.create_data(day))
        return a
    
    def get_articles_(self, article_id):
        return [v[article_id] for day, v in self.production.items()]
            
        
    def create_chart_data(self):
        return [
            {
                'label': article.name,
                'data': self.get_articles_(article.id)
            }
            for article in self.articles
        ]