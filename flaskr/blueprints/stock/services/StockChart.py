from .StockServices import StockServices, datetime

from flaskr.blueprints.articles.services.ArticlesService import ArticlesService

class StockChart(StockServices):
    def __init__(self, store_id=None, article_id=None, quantity=None, date=None):
        super().__init__(store_id, article_id, quantity, date)
        
        self.labels = self.get_stocks_dates()
        
    def create_date_labels(self):

        return [datetime.strftime(date.date, '%Y-%m-%d') for date in self.labels]
    
    def create_all_stock_list(self):
        stocks = []
        for date in self.labels:
            self.date = date.date
            stocks.append(self.get_data_for_stock_total())
        
        return stocks
    
    def create_datasets(self):
        articles = ArticlesService().get_all()
        
        return [{
            'label': article.name,
            'data': [i[article.id] for i in self.create_all_stock_list()]
        } for article in articles]