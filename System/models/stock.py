from .dbconnection import DbConnection
from datetime import datetime
from tinydb import Query
def get_timestamp(date = 0):

    if not date:
        date = str(datetime.today())

    date_obj = datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
    return date_obj.timestamp()



class Stock():
    pass

class StockArticles(DbConnection):
    """
    Use this class to create, edit, update or delete the articles
    of the DB
    """

    def __init__(self, db = 'System/databases/stock.json'):
        super().__init__(db)

        self.articles_names = self.get_all_articles()

    def get_all_articles(self) -> list:

        if 'articles' in self.db.tables():
            return self.db.table('articles').all()[0].get('articles', [])
        else:
            return []
        
    
    def check_if_articles_exist(self, article_name) -> bool:
        articles = self.get_all_articles()

        if articles:

            if article_name in articles:
                return True
        else:
            return False
            
    
    def insert_new_article(self, article_name) -> bool:

        """
        This function insert a new article in the database, if success
        return True

        article_name: str
        return: bool
        """

        def check_article_name(articles_name):
            invalid_char = ['-', '@', '#']
            if any(c in article_name for c in invalid_char):
                return False
            return True
            
        check_article_name(article_name)

        old_data = self.get_all_articles()
        
        if old_data:

            new_data = old_data
            

            if self.check_if_articles_exist(article_name):
                print('Articles already exist')
                return False
            else:
                new_data.append(article_name.replace(' ', ''))
                self.update_articles(new_data)
                return True
        else:
            new_data = [article_name]
            self.update_articles(new_data)
            return True
        
    
    def insert_multiples_articles(self, articles) -> None:
        """
        This function insert multiples article in the database,
        if some articles is already on the database will be added into the variable

        articles : list
        return : None"""

        duplicated_articles = list()

        if isinstance(articles, list):
            for article in articles:
                self.insert_new_article(article)
    
    
    def update_articles(self, new_data) -> None:
        """
        This funcion update all the database, be carefull
        new_data : list
        """
        old_articles = self.get_all_articles()
        new_articles_data = []

        if old_articles:
            return self.db.table('articles').update({'articles' : new_data})
        else:
            return self.db.table('articles').insert({'articles' : new_data})

        
    
    def delete_article(self, article_name):
        """
        This function delete a article in the database,
        if the article not exist, the function return False, otherwise return True
        article_name: str
        return: bool
        """

        if self.check_if_articles_exist(article_name):
            old_articles_list = self.get_all_articles()
            try:
                old_articles_list.remove(article_name)
                new_articles = old_articles_list
                self.update_articles(new_articles)
                return True

            except ValueError:
                print(f'{article_name} Not Found')
        else:
            return False
    
    def delete_multiples_articles(self, articles):
        """
        This funcion delete multples articles of the database
        if some articles doesn't exist they will be added into a variable
        
        articles :  list
        return : None

        """
        not_founded_articles = list()

        # Check if the user is passing multiples articles
        if isinstance(articles, list):
            print("You are passing a list, but this function just suport one 1 article each")
            self.delete_multiples_articles(articles)


        for article in articles:
            if self.delete_article(article):
                pass
            else:
                not_founded_articles.append(article)

        print(f'These articles was not found {not_founded_articles}')

class StoreStock(StockArticles):
    """
    Use this class to create, edit, delete or update in the 
    Store Stock DB
    """
    def __init__(self, db='System/databases/stock.json'):
        super().__init__(db)

    def generated_data(self, store, date, data):
        return {'store' : store, 
                'date' : get_timestamp(date),
                'articles' : data}
    
    
    def check_if_store_exist(self, store):
        """
        This function check if the store exist in DB
        store: str
        return: bool
        """
        store_name = DbConnection.stores.get(int)

        if store_name in self.db.tables():
            return True
        else:
            return False

    def create_store_stock(self, store, date = 0):
        """
        This function create a new table with the store articles in DB
        store: str
        return: None
        """

        store_name = DbConnection.get_store_name(int(store))

        stock_count = {}
        articles = self.articles_names

        for article in articles:
            stock_count[article] = 0

        if self.check_if_store_exist(store):
            print('Store already exist')
        else:
            self.db.table(store_name).insert(self.generated_data(int(store), date, stock_count))
        
        return stock_count

    def reset_stock_count(self, store, date = 0):
        store_name = DbConnection.get_store_name(store)

        reseted_stock = {}
        articles = self.articles_names

        for article in articles:
            reseted_stock[article] = 0

        if self.check_if_store_exist(store):
            self.db.table(store_name).update(self.generated_data(store, date, reseted_stock))

        else:
            print("This store, doesn't exist")

    
    def get_stocks_dates(self, store, inverted : bool = False, lenght : int = 0):
        from datetime import datetime
        dates = {}
        

        def convert_timestamp(timestamp):
            # Suponhamos que seu timestamp seja 1643145028 (um exemplo qualquer)
            date = datetime.fromtimestamp(timestamp)

            # Formate a data conforme necessário
            date = date.strftime('%d/%m/%Y - %H:%M:%S')

            return date

        stocks = self.get_store_stock(store, all = True)

        


        for stock in stocks:
            dates[stock.get('date')] = (convert_timestamp(stock.get('date')))

        if lenght:
            # Revert the dict to get the latest one first
            dates = dict(reversed(dates.items()))
            i = 0

            while len(dates) > lenght:
                dates.popitem()

        return dates if not inverted else dict(reversed(dates.items()))
 
    def get_store_stock(self, store, all = False, date = 0.0):
        
        """
        return the store stock count
        if you pass the parameter all as True, the function will return all the store stock count
        You also can use date filter
        store: str
        all = bool
        return: dict or list"""

        if isinstance(date, str) and '.' in date:
            date = float(date)

        store_name = DbConnection.get_store_name(int(store))

        stock_count = StoreStock().db.table(store_name).search(Query().store == int(store))

        if not stock_count:
            self.create_store_stock(int(store))
            stock_count = StoreStock().db.table(store_name).search(Query().store == int(store))

        if date:
            if date == 'last':
                return stock_count[-1].get('articles', {})
            
            elif date == 'reference':
                try:
                    return stock_count[-2].get('articles', {})
                except IndexError:
                    return stock_count[-1].get('articles', {})
        
            for stock in stock_count:
                if stock.get('date') == date:
                    return stock.get('articles')
            return {}
                
        if not all:
            return stock_count[-1].get('articles', {}) if stock_count else self.create_store_stock(int(store))
        else:
            return stock_count
    
    def get_difference(self, store, reference):
        """
        This function return the difference between the last stock count and the previous
        store: str
        return: dict
        """
        store_name = DbConnection.get_store_name(int(store))

        stock_count = self.get_store_stock(store, all=True)

        last_stock = stock_count[-1].get('articles', {})

        if len(stock_count) > 1:

            reference_stock = self.get_store_stock(store, date=reference)


            difference = {}

            for article, amount in last_stock.items():
                    difference[article] = amount - reference_stock.get(article, 0)

            return difference
        else:
            return {}
        

    def update_store_count(self, store, date, data):
        store_name = DbConnection.get_store_name(int(store))

        return self.db.table(store_name).update(self.generated_data(store, date, data))

    def enter_stock(self, store, date, data):

        store_name = DbConnection.get_store_name(int(store))
        old_stock_count = StoreStock().get_store_stock(store)

        if data.get('reference'):
            pass

        
        
        if isinstance(data, dict):
            for article, amount in data.items():
                
                try:
                    # Convert amount o int type and verify if amount is not negative
                    amount = int(amount) if amount else 0
                    # Verify if amount is less than 0
                    if isinstance(amount, int):
                        if amount < 0:
                            amount = 0
                except ValueError:
                    pass
                data[article] = amount

        new_stock_count = data

        self.db.table(store_name).insert(self.generated_data(store, date, new_stock_count))

    
    def create_data_to_chart(self, store, lenght):
        articles_label = self.articles_names

        data = []
        amount = []
        dates = set()

        lista = {}
        dates_chart = self.get_stocks_dates(store, False, lenght)
        for article in articles_label:

            lista[article] = []
            
            
            for date in self.get_stocks_dates(store, False, lenght).keys():
                
                
                dates.add(dates_chart[date])

                lista[article].append(self.get_store_stock(store, date=date).get(article, 0))

                amount.append(lista)

        for article in articles_label:
            data.append(
                {
                    'label' : article,
                    'data' : lista[article]
                }
            ) 
        
        return {'date' : list(dates), 'data' : data}

            

if __name__ == '__main__':
    import random
    a = StoreStock()
    a.delete_article('maionese4,344')