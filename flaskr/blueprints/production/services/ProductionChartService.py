# Standard library imports
from datetime import datetime, timedelta
import json

# Flask related imports
from flask_login import current_user

# Project specific imports
from flaskr.extensions import db

from flaskr.blueprints.articles.services.ArticlesService import ArticlesService
from .ProductionService import ProductionService



class ChartService():
    def __init__(self, store_id = None, how_many_days = None, date = None):
        self.how_many_dyas = how_many_days  or 7
        self.store_id = store_id or current_user.store_id
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        
        self.date_labels = self.create_date_labels_for_chart()
        self.articles = ArticlesService.get_all_producibles()
        
        self.all_days_productions = self.get_production_for_all_days() # Num of days

    def create_date_labels_for_chart(self) -> list:
        """ This function creates a list of dates that will be used for the chart.
        exe: if num_days = 6
            [2020-01-06, 2020-01-05, 2020-01-04, 2020-01-03, 2020-01-02, 2020-01-01]
            
            in this context these labels are used to set the columns in the chart
        """
        
        label = [self.date]
        
        label += [
            (datetime.strptime(self.date, '%Y-%m-%d') - timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range(1, self.how_many_dyas + 1)
            ]
        label.reverse()

        return label
        
        
    def convert_production_object_to_dict(self, day=None):
        """This method use the ProductionService to get the production object (from the database) for a given day.
        then convert it to a dictionary.
        from it: [(3, Decimal('8')), (4, Decimal('4')), (5, Decimal('7')), (6, Decimal('5')), (7, Decimal('12')), (8, Decimal('2'))]
        to: {3: 8, 4: 4, 5: 7, 6: 5, 7: 12, 8: 2} where key is an article_id and value is a quantity.
        
        The importance of this method is that if some day doesn't have any production it will return an dict where key
        continues being the article_id e and the quantity is set to 0 (Using the get method from buildin python).
        To undestand better this situation we need to know that when an day doesnt have any production the production objetct
        doesnt give as the articles that is empty, it just retorn an empty list, that doesnt help with the chart cause we
        can not get the sequecial production of an article:
        exemple if we want get the last 3 days of apple production, if any of these 3 days doesnt be in database
        instead we get the 0 quantity, we we get a None, so this method is used to get an 0 instead an None value of all the 
        articles avalible in our database
        """
        
        day_production = ProductionService(date=day).get_already_prodeced()

        production_dict = { p.article_id: int(p.quantity) for p in day_production }

        return {
            article.id: production_dict.get(article.id, 0)
            for article in self.articles
        }
        
    def get_production_for_all_days(self):
        dataset = {}
        
        for day in self.date_labels:
            
            day = datetime.strptime(day, '%Y-%m-%d')
            
            dataset[datetime.strftime(day, '%Y-%m-%d')] = (self.convert_production_object_to_dict(day=day))

        return dataset
    
    def get_article_data_of_each_day(self, article_id : str | int) -> list:
        """ This method give us a list with amount of article in all the previous days
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