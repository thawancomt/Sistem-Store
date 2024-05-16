from tinydb import TinyDB, Query
from tinydb.operations import increment
from hashlib import sha256

from datetime import datetime


class DbConnection():
    permissive_keys_for_create_users = [
        'username',
        'password',
        'level',
        'email',
        'store',
        'when_was_created',
        'last_login'
    ]

    stores = {
        3: 'Colombo',
        5: 'Odivelas',
        11: 'Campo de Ourique',
        25: 'Baixa Chiado',
        13: 'Alvalade',
        17: 'Amoreiras',
        19: 'Saldanha',
        23: 'Areeiro',
        29: 'Avenida',
        31: 'Entrecampos',

    }

    articles = {
        'big_ball': 'Big Ball',
        'small_ball': 'Small Ball',
        'garlic_bread': 'Garlic bread',
        'mozzarela': 'Mozzarela',
        'edamer': 'Edamer',
        'bacon': 'Bacon',
        'goronzola': 'Goronzola',
        'pepperoni': 'Pepperoni',
    }

    default_production = {article: 0 for article in articles}

    def __init__(self, db):
        self.db_text = db
        self.db = TinyDB(db, indent=4)
        self.tables = self.db.tables()

    def __del__(self):
        self.db.close()


    # Get functions
    @staticmethod
    def get_store_name(store_id : int) -> str:
        """
        Get the store name based on the dict of store's ID
        """
        store_id = int(store_id)
        
        
        if store_id not in DbConnection.stores:
            raise ValueError('Store not found')

        return DbConnection.stores.get(store_id, 0)
    
    def get_user_data(self, who):

        guest = {
            'username': 'guest',
            'password': 'guest',
            'email': 'guest@gmail.com',
            'store': '0',
            'level': 'worker',
            'when_was_created': '1999-01-01',
        }

        for table in self.tables:
            result = self.db.table(table).search (
                (Query().username == who.username) | (Query().email == who.email)
            )
        
        return result[0] if result else guest
    
    
    def get_all_users(self):
        users = []

        for table in self.tables:
            users.extend(self.db.table(table).search(Query().username != ''))

        return users

    def get_users_by_search(self, search):
        users = self.get_all_users()

        filtered_users = []

        for user in users:
            if search.lower() in user.get('username').lower():
                filtered_users.append(user)

        return filtered_users


    def get_users_by_store(self, store):
        users = self.get_all_users()

        filtered_users = []

        for user in users:
            if store == user.get('store', 0):
                filtered_users.append(user)

        return filtered_users

        
    def get_day_consume(self, store, date):

        store_name = DbConnection.get_store_name(store)

        result = self.db.table(store_name).search((Query().date == date))

        if result:
            if result[0].get('date'):
                del result[0]['date']

        return result[0] if result else {}
        

    def get_wasted(self, store, date):
        store_name = DbConnection.get_store_name(store)

        result = self.db.table(store_name).search(Query().date == date)

        return result[0] if result else {}
    

    def get_day_production(self, store, date):
        store_name = DbConnection.get_store_name(store)

        result = self.db.table(store_name).search(Query().date == str(date))

        return result[0].get('production',  {}) if result else {}

    # Insert functions

        
    def insert_stock(self, data):
        self.db = TinyDB('flaskr/databases/stock.json', indent=4)

        self.db.insert(data)

    def insert_consumes(self, who, date, store, data):
        if data.get('who_consume'):
            del data['who_consume']

        for article, amount in data.items():

            if amount.isnumeric():
                amount = int(amount)
                data[article] = amount
            else:
                try:
                    data[article] = int(amount)
                except:
                    return False


        store_name = self.stores[store]

        result = self.get_day_consume(store, date)

        if data.get('who_consume'):
            del data['who_consume']

        if result:
            self.update_consume(who, date, store, data)
        else:
            self.db.table(store_name).insert({'date': date, who: data})

    def insert_wasted(self, who, date, store, data):

        for article, amount in data.items():
                try:
                    data[article] = int(amount)
                except ValueError:
                    return False

        store_name = DbConnection.get_store_name(store)

        result = self.get_wasted(store, date)

        # delete the who_consume key to send directly to the database
        if data.get('who_consume'):
            del data['who_consume']

        if result:
            self.update_wasted(who, date, store, data)
        else:
            self.db.table(store_name).insert({'date': date, who: data})

    def insert_production(self, store, date, data):

        store_name = DbConnection.get_store_name(store)

        produced = DbConnection(self.db_text).get_day_production(store, date)

        for article, amount in data.items():
            if isinstance(amount, str | float):
                raise TypeError('The amount of the article must be an integer')

        if not date:
            return {}

        if not produced:
            self.db.table(store_name).insert({'date': date, 'production': data})
        else:
            self.__update_production(store, date, produced, data)

    def check_user_exist(self, username: str = '', email: str = ''):

        return True if self.search_username(username) or self.search_email(email) else False

    # Update functions
    def update_user(self, who, new_info):

        username = new_info.get('username')
        email = new_info.get('email')
        storeID = self.get_user_data(who)['store']
        print('*******************************',storeID)
        store_name = self.stores[storeID]
        try:
            if self.check_user_exist(username, email):
                raise 'This User Already Exist'
        except:
            return False

        keys_to_delete = []

        for key, value in new_info.items():
            if not value:
                keys_to_delete.append(key)
            if key == 'password':
                new_info[key] = sha256(value.encode()).hexdigest()

        for key in keys_to_delete:
            del new_info[key]

        self.db.table(store_name).update(new_info, Query().email == who.email)
    
    def __update_production(self, store, date, old_data, new_data):
        """_summary_

        Args:
            store (_type_): _description_
            date (_type_): _description_
            old_data (_type_): _description_
            new_data (_type_): _description_
        """

        store_name = DbConnection.get_store_name(store)

        generated_data = {}

        for article, amount in old_data.items():
            generated_data[article] = amount

        for article, amount in new_data.items():
            if article in generated_data:
                generated_data[article] += amount
            else:
                generated_data[article] = amount

        self.db.table(store_name).update({'production': generated_data}, Query().date == date)
    
    def update_consume(self, who, date, store, new_data):

        store_name = DbConnection.get_store_name(store)

        if new_data:

            old_data = self.get_day_consume(store, date).get(who, {})



            for article, amount in old_data.items():
                new_data[article] += int(amount)

            self.db.table(store_name).update({who: new_data}, Query().date == date)

    
    def update_wasted(self, who, date, store, data):

        store_name = DbConnection.get_store_name(store)
        old_data = self.get_wasted(store, date).get(who, {})

        if data:
            for article, amount in old_data.items():
                data[article] += int(amount)

            self.db.table(store_name).update({who: data}, Query().date == date)

    

    def search_username(self, username):
        for table in self.tables:
            result = self.db.table(table).search(Query().username == username)
            if result:
                return result


    def search_email(self, email):
        for table in self.tables:
            result = self.db.table(table).search(Query().email == email)
            if result:
                return result
            
    def delete_user(self, store, email):

        print(f'This is the email {email}')

        store_name = DbConnection.get_store_name(store)

        return self.db.table(store_name).remove(Query().email == email)

