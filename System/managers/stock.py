if __name__ == '__main__' or __name__ == 'stock.py':
    from dbconnection import DbConnection
else:
    from System.managers.dbconnection import DbConnection

class Stock():
    pass

class StockArticles(DbConnection):
    def __init__(self, db = 'System/databases/stock.json'):
        super().__init__(db)

    def get_all_articles(self) -> list:
        return self.db.table('articles').all()[0].get('articles')
    
    def check_if_articles_exist(self, article_name) -> bool:
        articles = self.get_all_articles()

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
        
        old_data = self.get_all_articles()

        new_data = old_data
        new_data.append(article_name)

        if self.check_if_articles_exist(article_name):
            print('Articles already exist')
            return False
        else:
            self.update_articles(new_data)
            return True
    
    def insert_multiples_articles(self, articles, duplicated = False) -> None:
        """
        This function insert multiples article in the database,
        if some articles is already on the database will be added into the variable

        articles : list
        return : None"""

        duplicated_articles = list()

        for article in articles:
            if self.insert_new_article(article):
                pass
            else:
                duplicated_articles.append(article)
    
    def update_articles(self, new_data) -> None:
        """
        This funcion update all the database, be carefull
        new_data : list
        """
        old_articles = self.get_all_articles()

        return self.db.table('articles').update({'articles' : new_data})
    
    def delete_article(self, article_name):
        """
        This function delete a article in the database,
        if the article not exist, the function return False, otherwise return True
        article_name: str
        return: bool
        """

        # Check if the user is passing multiples articles
        if isinstance(article_name, list):
            print("You are passing a list, but this function just suport one 1 article each")
            self.delete_multiples_articles(article_name)

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

        for article in articles:
            if self.delete_article(article):
                pass
            else:
                not_founded_articles.append(article)

        print(f'These articles was not found {not_founded_articles}')