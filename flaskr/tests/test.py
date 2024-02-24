import unittest

from flaskr.dbconnection import DbConnection
from flaskr.models.production import Production


class test_Production(unittest.TestCase):

    def setUp (self):
        self.db = DbConnection ('testEmptyInsert.json')

    def tearDown (self):
        self.db.db.close ()

    def test_insert_production_emptyFile (self):
        self.db.db.drop_tables ()

        self.db.insert_production (3, '2020-01-01', {'bacon': 2})

        expected = {'bacon': 2}

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), expected)

    def test_insert_production_emptyFile_Production (self):
        self.db.db.drop_tables ()

        self.db.insert_production (3, '2020-01-01', {'bacon': 2})

        expected = {'bacon': 2}

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), expected)

    def test_insertProduction_Already_produced (self):
        self.db.db.drop_tables ()

        self.db.insert_production (3, '2020-01-01', {'bacon': 4})
        self.db.insert_production (3, '2020-01-01', {'bacon': 4})

        expected = {'bacon': 8}

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), expected)

    def test_InsertProductionWithPositiveAndNegativeValues (self):
        self.db.db.drop_tables ()

        self.db.insert_production (3, '2020-01-01', {'bacon': 4, 'cheese': -2})
        self.db.insert_production (3, '2020-01-01', {'bacon': -4, 'cheese': 2})

        expected = {'bacon': 0, 'cheese': 0}

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), expected)

    def test_insertingStr2 (self):
        self.db.db.drop_tables ()

        with self.assertRaises (TypeError):
            self.db.insert_production (3, '2020-01-01', {'bacon': '4'})
            self.db.insert_production (3, '2020-01-01', {'bacon': 4})

    def test_insertingFloat (self):
        self.db.db.drop_tables ()
        with self.assertRaises (TypeError):
            self.db.insert_production (3, '2020-01-01', {'bacon': 4.5})

    def test_get_day_production (self):
        self.db.db.drop_tables ()

        self.db.insert_production (3, '2020-01-01', {'bacon': 4})
        self.db.insert_production (3, '2020-01-01', {'cheese': 2})
        self.db.insert_production (3, '2020-01-01', {'salsage': 14})
        self.db.insert_production (3, '2020-01-01', {'peperoni': 2})

        expected = {'bacon': 4, 'cheese': 2, 'salsage': 14, 'peperoni': 2}

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), expected)

    def test_get_day_production_empty (self):
        self.db.db.drop_tables ()

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), {})

    def test_insert_Production_With_EmptyDate (self):
        self.db.db.drop_tables ()

        self.db.insert_production (3, '', {'bacon': 4})

        self.assertEqual (self.db.get_day_production (3, ''), {})

    def test_insert_empty_production (self):
        self.db.db.drop_tables ()

        self.db.insert_production (3, '2020-01-01', {})

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), {})

    def test_insert_production_with_empty_id (self):
        self.db.db.drop_tables ()

        with self.assertRaises (ValueError):
            self.db.insert_production ('', '2020-01-01', {'bacon': 4})

    def test_insert_production_with_empty_date (self):
        self.db.db.drop_tables ()

        self.db.insert_production (31, '', {'bacon': 4})

        expected = {}

        self.assertEqual (self.db.get_day_production (31, ''), expected)

    def test_insert_production_with_empty_date_and_production (self):
        self.db.db.drop_tables ()

        self.db.insert_production (31, '', {})

        expected = {}

        self.assertEqual (self.db.get_day_production (31, ''), expected)

    def test_chart_creation (self):
        self.db.db.drop_tables ()

    def test_get_stores_names (self):
        self.db.stores = {1: 'test1',
                          2: 'test2',
                          3: 'test3',
                          4: 'teste4'}

        expected_names = ['test1', 'test2', 'test3']

        for i in range (1, 4):
            self.assertEqual (self.db.stores [i], expected_names [i - 1])


class test_ProductionByClass (unittest.TestCase):
    def setUp (self) -> None:
        self.pr = Production ('2020-01-01')
        self.pr.store = 3

        self.db = DbConnection ('testEmptyInsert.json')

    def test_insert_production (self):
        self.db.db.drop_tables ()

        self.pr.store = 3
        self.pr.date = '2020-01-01'
        self.pr.data = {'chicken': 4}

        self.pr.send_production ()

        expected = {'chicken': 4}

        self.assertEqual (self.pr.get_already_produced (3), expected)

    def test_insert_with_already_produced (self):
        self.db.db.drop_tables ()

        self.pr.store = 3
        self.pr.date = '2020-01-01'
        self.pr.data = {'chicken': 4}

        self.pr.send_production ()

        self.pr.data = {'chicken': 4}

        self.pr.send_production ()

        expected = {'chicken': 8}

        self.assertEqual (self.pr.get_already_produced (3), expected)

    def test_insert_production_with_empty_date (self):
        self.db.db.drop_tables ()

        with self.assertRaises (ValueError):
            self.pr.store = 3
            self.pr.date = ''
            self.pr.get_already_produced (3)

    def test_not_listed_store (self):
        with self.assertRaises (KeyError):
            self.pr.store = 0

    def test_insert_multiples_dates_and_inserts (self):
        self.db.db.drop_tables ()

        self.pr.data = {'bacon': 1, 'mozzarela': 5}

        self.pr.store = 3

        self.pr.send_production ()
        self.pr.send_production ()

        self.pr.date = '2020-01-02'

        self.pr.data = {'bacon': 1, 'mozzarela': 5}

        self.pr.store = 3

        self.pr.send_production ()
        self.pr.send_production ()

        expected = {'bacon': 2, 'mozzarela': 10}

        self.assertEqual (self.db.get_day_production (3, '2020-01-01'), expected)
        self.assertEqual (self.db.get_day_production (3, '2020-01-02'), expected)

    def test_chart_creation (self):
        self.db.db.drop_tables ()

        self.pr.store = 3

        self.pr.date = '2020-01-01'

        self.pr.data = {'big_ball': 2, 'small_ball': 20}

        self.pr.send_production ()

        self.pr.date = '2020-01-02'

        self.pr.data = {'big_ball': 4, 'cheese': 30}

        self.pr.send_production ()

        self.pr.date = '2020-01-03'
        self.pr.data = {'big_ball': 5, 'small_ball': 12}
        self.pr.send_production ()

        self.pr.date = '2020-01-04'

        expected = {'labels': ['2020-01-01', '2020-01-02', '2020-01-03'],
                    'datasets': [
                        {'label': 'big_ball',
                         'data': [2, 4, 5]},
                        {'label': 'small_ball',
                         'data': [20, 0, 12]},
                        {'label': 'cheese',
                         'data': [0, 30, 0]}
                    ]}

        self.assertEqual (self.pr.create_data_to_ball_usage_chart (3, -3), expected)

    def test_creation_chart_with_empty_production (self):
        self.db.db.drop_tables ()

        self.pr.date = '2020-01-03'

        expected = {'labels': ['2020-01-01', '2020-01-02'],
                    'datasets': []}

        self.assertEqual (self.pr.create_data_to_ball_usage_chart (3, -2), expected)

