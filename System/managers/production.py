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
        
        data_to_return = {'big_ball' : [],
                'small_ball' : [],
                'garlic_bread' : [],
                'mozzarela' : [],
                'edamer' : []}

        for day in before_week:

            self.date = day
            result = self.get_already_produced(store)

            dates.append(day)

            for key, value in self.articles.items():
                data_to_return[key].append(result[key])

            result = self.get_already_produced(store)

        data_to_return['dates'] = dates
        return data_to_return


class Consumes():
    def __init__(self):
        self.worker: str = ''
        self.store: int = 0
        self.date: str = ''
        self.data: str = ''

    def send_consume(self):
        DbConnection('databases/consumes.json').insert_consumes(who=self.worker,
                                                                date=self.date,
                                                                store=self.store,
                                                                data=self.data)

    def get_consume_by_day(self, store, date):
        return DbConnection('databases/consumes.json').get_day_consume(store, date)


class Stores(Production):

    def __init__(self):
        super().__init__(self.get_already_produced)
        self.store = 0


if __name__ == '__main__':

    from dbconnection import DbConnection

    print(Production("2023-12-09").create_data_to_ball_usage_chart(11, -7))

    # print(Consumes().get_consume_by_day(5, 22))
