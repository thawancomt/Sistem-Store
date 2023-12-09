if not __name__ == '__main__':
    from managers.dbconnection import DbConnection


class Production():
    articles = {
        'big_ball': 'Big Ball',
        'small_ball': 'Small Ball',
        'garlic_bread': 'Garlic bread',
        'mozzarela': 'Mozzarela',
        'edamer': 'Edamer',


    }
    stores = {
        3: 'Colombo',
        5: 'Odivelas',
        11: 'Campo de Ourique',
        25: 'Baixa Chiado'
    }

    def __init__(self, date, data={}):
        self.store = 0
        self.data = data  # Data
        self.date = date  # Date

    def send_production(self):
        DbConnection('databases/production.json').insert_production(
            self.store, self.date, self.data)

    def get_already_produced(self, store):
        return DbConnection('databases/production.json').get_day_production(store, self.date)

class Consumes():
    def __init__(self):
        self.worker : str  = ''
        self.store : int  = 0
        self.date : str = ''
        self.data : str = ''
        

    
    def send_consume(self):
        DbConnection('databases/consumes.json').insert_consumes(who = self.worker,
                                                                date = self.date,
                                                                store = self.store,
                                                                data = self.data)
        
    def get_consume_by_day(self, store, date):
        return DbConnection('databases/consumes.json').get_day_consume(store, date)
        
class Stores(Production):

    def __init__(self):
        super().__init__(self.get_already_produced)
        self.store = 0

if __name__ == '__main__':

    from dbconnection import DbConnection
    
    teste = Consumes()

    teste.worker = 'Thawan HG'
    teste.store = 11
    teste.date = 22
    teste.data = {'slices': 30, 'bread' : 20}
    teste.send_consume()

    # print(Consumes().get_consume_by_day(5, 22))