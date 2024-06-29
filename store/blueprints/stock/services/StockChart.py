from .StockServices import StockServices, datetime

from store.blueprints.articles.services.ArticlesService import ArticlesService

class StockChart(StockServices):
    def __init__(self, store_id=None, article_id=None, quantity=None, date=None, days = None):
        super().__init__(store_id, article_id, quantity, date)
        self.days = days or 90
        self.labels = self.get_stocks_dates()
        
    def create_date_labels(self):
        date_labels = [datetime.strftime(date.date, '%m-%d %H:%M') for date in self.labels][:self.days]

        return date_labels
    
    def create_all_stock_list(self):
        stocks = []
        for date in self.labels:
            self.date = date.date
            stocks.append(self.get_data_for_stock_total())
        
        return stocks
    
    def create_datasets(self):
        
        return [{
            'label': article.name,
            'data': [i.get(article.id, 0) for i in self.create_all_stock_list()],
            'tension': 0.2,
        } for article in self.articles]