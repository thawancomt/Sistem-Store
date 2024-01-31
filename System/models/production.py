from .dbconnection import DbConnection

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
        DbConnection('System/databases/production.json').insert_production(
            self.store, self.date, self.data)

    def get_already_produced(self, store):
        return DbConnection('System/databases/production.json').get_day_production(store, self.date)

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

        def increment_date(day: int) -> str:  # OK
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

        before_week: list = []

        for day in range(length, end):
            before_week.append(increment_date(day))

        before_week.append(initial_date_to_show_in_final_of_chart)

        dates = []

        data_to_return = {'big_ball': [],
                          'small_ball': [],
                          'garlic_bread': [],
                          'mozzarela': [],
                          'edamer': [],
                          'articles': []}
        labels_col = []

        for day in before_week:

            self.date = day
            result = self.get_already_produced(store)

            dates.append(day)

            for key, value in self.articles.items():

                if not value in data_to_return['articles']:
                    data_to_return['articles'].append(value)

                data_to_return[key].append(result[key])

            result = self.get_already_produced(store)

        for key, value in self.articles.items():
            labels_col.append({'label': value,
                               'data': data_to_return[key]})

        data_to_return['dates'] = dates

        data_to_return['data_labels'] = labels_col

        return data_to_return


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
        DbConnection('System/databases/consumes.json').insert_consumes(who=self.worker,
                                                                date=self.date,
                                                                store=self.store,
                                                                data=self.data)

    def get_consume_by_day(self, store, date):
        return DbConnection('System/databases/consumes.json').get_day_consume(store, date)

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


if __name__ == '__main__':

    from dbconnection import DbConnection

    teste = Consumes()

    print(teste.create_data_to_consume_chart(3, '2024-01-25'))


class Wasted():
    def __init__(self, date_for, store):
        self.store = store
        self.date_for = date_for
        self.data = {}
        self.worker = str

    def enter_wasted(self):
        return DbConnection('System/databases/waste.json').insert_wasted(who=self.worker,
                                            date=self.date_for,
                                            store=self.store,
                                            data=self.data)
    def update_wasted(self):
        return DbConnection('System/databases/waste.json').update_wasted(who=self.worker,
                                            date=self.date_for,
                                            store=self.store,
                                            data=self.data)
    
