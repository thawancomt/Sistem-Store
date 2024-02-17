import unittest
from dbconnection import DbConnection



class Test_Production(unittest.TestCase):
    
    def setUp(self):
        self.db = DbConnection('testEmptyInsert.json')
        

    def tearDown(self):
        self.db.db.close()

    
    def test_insert_production_emptyFile(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {'bacon': 2})

        expected = {'bacon': 2}

        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), expected)
    
    def test_insert_production_emptyFile_Production(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {'bacon': 2})

        expected = {'bacon': 2}

        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), expected)

    
    def test_insertProduction_Already_produced(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {'bacon': 4})
        self.db.insert_production(3, '2020-01-01', {'bacon': 4})

        expected = {'bacon': 8}

        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), expected)
        
    
    def test_InsertProductionWithPositiveAndNegativeValues(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {'bacon': 4, 'cheese': -2})
        self.db.insert_production(3, '2020-01-01', {'bacon': -4, 'cheese': 2})

        expected = {'bacon': 0, 'cheese': 0}

        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), expected)
    
    def test_insertingStr2(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {'bacon': '4'})

        expected = {'bacon': '4'}
        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), expected)
    
    
    

    def test_insertingFloat(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {'bacon': 4.5})

        expected = {'bacon': 4.5}
        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), expected)

    
    def test_get_day_production(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {'bacon': 4})
        self.db.insert_production(3, '2020-01-01', {'cheese': 2})
        self.db.insert_production(3, '2020-01-01', {'salsage': 14})
        self.db.insert_production(3, '2020-01-01', {'peperoni': 2})

        expected = {'bacon': 4, 'cheese': 2, 'salsage': 14, 'peperoni': 2}

        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), expected)
    

    def test_get_day_production_empty(self):

        self.db.db.drop_tables()

        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), {})

    
    def test_insert_Production_With_EmptyDate(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '', {'bacon': 4})

        self.assertEqual(self.db.get_day_production(3, ''), {})


    def test_insert_empty_production(self):

        self.db.db.drop_tables()

        self.db.insert_production(3, '2020-01-01', {})

        self.assertEqual(self.db.get_day_production(3, '2020-01-01'), {})

    
    def test_insert_production_with_empty_id(self): 

        self.db.db.drop_tables()

        with self.assertRaises(ValueError):
            self.db.insert_production('', '2020-01-01', {'bacon': 4})


    def test_insert_production_with_empty_date(self): 

        self.db.db.drop_tables()

        self.db.insert_production(31, '', {'bacon': 4})

        expected = {}

        self.assertEqual(self.db.get_day_production(31, ''), expected)

    def test_insert_production_with_empty_date_and_production(self): 

        self.db.db.drop_tables()

        self.db.insert_production(31, '', {})

        expected = {}

        self.assertEqual(self.db.get_day_production(31, ''), expected)

    def test_chart_creation(self):
        self.db.db.drop_tables()
    
    def test_get_stores_names(self):
        self.db.stores = {1 : 'test1',
                          2 : 'test2',
                          3 : 'test3',
                          4 : 'teste4'}
        
        expected_names = ['test1', 'test2', 'test3']
    
        for i in range(1, 4):
            self.assertEqual(self.db.stores[i], expected_names[i-1])

    
unittest.TestLoader.sortTestMethodsUsing = None
unittest.main(verbosity=4)