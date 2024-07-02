# Standard library imports
from datetime import datetime, timedelta
import json

# Flask related imports
from flask_login import current_user

# Project specific imports
from store.extensions import db
from store.blueprints.articles.services.ArticlesService import ArticlesService
from ..services.ProductionService import ProductionService

class ProductionChartService(ProductionService):
    def __init__(self, date, days, store):
        super().__init__(store_id=store)
        self.date = date
        self.days = days
        self.store = store
        self.articles = ArticlesService.get_all_producibles()
        
        ### Chart
        
        self.date_labels = self.create_labels()
        self.dataset = self.create_dataset_for_chart()
        
    def create_labels(self):
        date_labels = []
        
        date_labels.extend(
            (
                datetime.strptime(self.date, '%Y-%m-%d') - timedelta(days=day)
            ).strftime('%Y-%m-%d')
            for day in range(self.days + 1)
        )
        date_labels.reverse()
        
        return date_labels
    
    
    def convert_production_object_to_dict(self, production) -> dict[int:int]:
        """This method uses the ProductionService to get the production object (from the database) for a given day,
        then converts it to a dictionary.
        from: [(3, Decimal('8')), (4, Decimal('4')), (5, Decimal('7')), (6, Decimal('5')), (7, Decimal('12')), (8, Decimal('2'))]
        to: {3: 8, 4: 4, 5: 7, 6: 5, 7: 12, 8: 2} where the key is an article_id and the value is a quantity.
        
        The importance of this method is that if some day doesn't have any production, it will return a dict where the key
        continues being the article_id and the quantity is set to 0 (using the get method from built-in python).
        """
        
        production_dict = {
            production.article_id: int(production.quantity)
            for production in production}

        return {
            article.id: production_dict.get(article.id, 0)
            for article in self.articles
        }
    
    def get_production_for_all_days(self):
        from pprint import pprint
        
        productions = {}
        
        for day in self.date_labels:
            self.date = day
            productions[day] = self.get_already_prodeced()
            
        return productions
    

    def create_dataset(self):
        articles_dataset = { article.name : [] for article in self.articles}
        productions = self.get_production_for_all_days()
        
        for day, production in productions.items():
            production_dict = self.convert_production_object_to_dict(production)

            for article in self.articles:
                articles_dataset[article.name].append(production_dict.get(article.id, 0))
        
        return articles_dataset
    
    def create_dataset_for_chart(self):
        return {
            'labels' : self.date_labels,
            'datasets' : [
                {
                    'label' : article,
                    'data' : data
                }
                for article, data in self.create_dataset().items()
            ]
        }

    

    