# Standard library imports
from datetime import datetime, timedelta
import json

# Flask related imports
from flask_login import current_user

# Project specific imports
from flaskr.extensions import db
from flaskr.blueprints.articles.services.ArticlesService import ArticlesService
from ..services.ProductionService import ProductionService


class ChartService(ProductionService):
    def __init__(self, store_id=None, how_many_days=None, date=None):
        super().__init__(store_id=store_id)
        self.how_many_days = how_many_days or 7
        self.store_id = store_id or current_user.store_id
        self.date = date
        
        self.date_labels = self.create_date_labels_for_chart()
        self.articles = ArticlesService.get_all_producibles()
        
        self.all_days_productions = self.get_production_for_all_days() # Num of days

    def create_date_labels_for_chart(self) -> list:
        """ This function creates a list of dates that will be used for the chart.
        exe: if num_days = 6
            [2020-01-06, 2020-01-05, 2020-01-04, 2020-01-03, 2020-01-02, 2020-01-01]
            
            in this context these labels are used to set the columns in the chart
        """
        
        base_date = self.date
        labels = [
            (datetime.strptime(base_date, '%Y-%m-%d') - timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range(1, self.how_many_days + 1)
            ]
        labels.reverse()
        labels.append(base_date)

        return labels
    
    
    def convert_production_object_to_dict(self, date):
        """This method uses the ProductionService to get the production object (from the database) for a given day,
        then converts it to a dictionary.
        from: [(3, Decimal('8')), (4, Decimal('4')), (5, Decimal('7')), (6, Decimal('5')), (7, Decimal('12')), (8, Decimal('2'))]
        to: {3: 8, 4: 4, 5: 7, 6: 5, 7: 12, 8: 2} where the key is an article_id and the value is a quantity.
        
        The importance of this method is that if some day doesn't have any production, it will return a dict where the key
        continues being the article_id and the quantity is set to 0 (using the get method from built-in python).
        """
        
        self.date = date
        
        day_production = self.get_already_prodeced()
        production_dict = {p.article_id: int(p.quantity) for p in day_production}

        return {
            article.id: production_dict.get(article.id, 0)
            for article in self.articles
        }

    def get_production_for_all_days(self):
        return {
            date: self.convert_production_object_to_dict(date = date)
            for date in self.date_labels
        }
    
    def get_article_data_of_each_day(self, article_id: str | int) -> list:
        """ This method gives us a list with the amount of article in all the previous days
        we use this list to pass into our chart"""
        return [article_quantity[article_id] for day, article_quantity in self.all_days_productions.items()]
            
    def create_chart_datasets(self):
        return [
            {
                'label': article.name,
                'data': self.get_article_data_of_each_day(article.id)
            }
            for article in self.articles
        ]
