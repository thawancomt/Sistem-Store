from flaskr.dbconnection import DbConnection
default_path = {'production': 'flaskr/databases/production.json',
                'consumes': 'flaskr/databases/consumes.json',
                'waste': 'flaskr/databases/waste.json'}

class Production():

    articles = DbConnection.articles

    stores = DbConnection.stores

    def __init__(self, date = '' , data = {}):

        self.store : int
        self.data = data  # Data
        self.date = date  # Date

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        if value == '':
            raise ValueError('Date cannot be empty')
        self._date = value

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if not isinstance(value, dict):
            raise ValueError('data must be a dictionary')
        self._data = value

    @property
    def store(self):
        return self._store
    
    @store.setter
    def store(self, value):
        if value not in self.stores:
            raise KeyError('This store doesnt exist in the setup')
        self._store = value



    def send_production(self):
        return DbConnection(default_path.get('production')).insert_production(
            self.store, self.date, self.data)
    

        
    
    def get_already_produced(self, store):
        return DbConnection(default_path.get('production')).get_day_production(store, self.date)

    
    def create_data_to_ball_usage_chart(self, store, length, end=1):
        """receive a list to create a chart

        Args:
            length (int): how many columns to create (before days)
            example:
                length = 3 with date = 2000-01-10 will return
                    [[2000-01-09, 2000-01-08, 2000-01-07]
                    and [the usage balls of each day]]

        Returns:
            list: Will return a list with dates of day before

        """
        initial_date_to_show_in_final_of_chart = self.date

        def increment_date(day: int) -> str:
            from datetime import datetime, timedelta

            try:
                date = datetime.strptime(self.date, '%Y-%m-%d').date()

                incremented_date = str(date + timedelta(days=day))

                return incremented_date

            except ValueError:
                raise ('Invalid date')

        if length > 0:
            end = length + 1
            length = 1
        else:
            end = 0

        dates = []

        for day in range(length, end):
            dates.append(increment_date(day))
        
        articles = {}

        # 1 loop
        # Used to navigation in all days
        for day in dates:
            self.date = day
            produced = self.get_already_produced(store)

            # This internal loop is to add all articles to artciles dict
            # to understand the needed of separated loop, day 1 may have an articles
            # and day 2 don't
            # so we need to pass all day to verify all articles
            for article in produced.keys():
                if article not in articles:
                    articles[article] = []
                    
        # Finally when all articles was checked and added into the dict
        # We can pass in all days again and catch this articles production
        # if this production doesnt have an production in the day, return 0
        
        for day in dates:
            self.date = day
            for article in articles:
                articles[article].append(self.get_already_produced(store).get(article, 0))

        return {'labels' : ['g', 'k'],
                'datasets' : [
                    ({'label' : item,
                      'data' : articles.get(item)}) for item in articles
                ]}


class Consumes():

    permissive_keys_to_enter_waste = [
        'big_ball',
        'small_ball',
        'garlic_bread',
        'slices'
    ]

    def __init__(self):
        self.worker: str = ''
        self.store: int = 0
        self.date: str = ''
        self.data: str = ''

    def send_consume(self):
        DbConnection(default_path.get('consumes')).insert_consumes(who=self.worker,
                                                                date=self.date,
                                                                store=self.store,
                                                                data=self.data)

    def get_consume_by_day(self, store, date):
        return DbConnection(default_path.get('consumes')).get_day_consume(store, date)

    def create_data_to_consume_chart(self, store, date):

        # Try to get already consumed amount, if indexError, return empty values
        workers_consume = self.get_consume_by_day(store, date)

        result = {
            'data': [],
            'workers': []
        }

        for worker, data in workers_consume.items():
            result['workers'].append(worker)

        slices = []
        bread = []

        for worker in result['workers']:
            bread.append(workers_consume[worker]['bread'])
            slices.append(workers_consume[worker]['slice'])
            
        result = {'data': [{'label' : 'slice', 'data' : slices,}, {'label': 'bread', 'data' : bread}], 'workers': result['workers']}
        
        return result




class Wasted():
    def __init__(self, date_for, store):
        self.store = store
        self.date_for = date_for
        self.data = {}
        self.worker = str

    def enter_wasted(self):
        return DbConnection(default_path.get('waste')).insert_wasted(who=self.worker,
                                            date=self.date_for,
                                            store=self.store,
                                            data=self.data)
    def update_wasted(self):
        return DbConnection(default_path.get('waste')).update_wasted(who=self.worker,
                                            date=self.date_for,
                                            store=self.store,
                                            data=self.data)
    

