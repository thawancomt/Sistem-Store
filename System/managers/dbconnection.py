from tinydb import TinyDB, Query
from tinydb.operations import increment


class DbConnection():
    permissive_keys_for_create_users = [
        'username',
        'password',
        'level',
        'email',
        'store',
        'when_created',
        'last_login'
    ]

    stores = {
        3: 'Colombo',
        5: 'Odivelas',
        11: 'Campo de Ourique',
        25: 'Baixa Chiado'
    }

    default_production = {
        'big_ball': 0,
        'small_ball': 0,
        'garlic_bread': 0,
        'mozzarela': 0,
        'edamer': 0,
    }

    def __init__(self, db):
        self.db = TinyDB(db, indent=4)

    def search_username(self, username):
        result = self.db.search(Query().username == username)
        return result

    def search_email(self, email):
        result = self.db.search(Query().email == email)
        return result

    def insert_user(self, data):
        """Insert a new user into the database

        Args:
            data dict: User data need be a dict

        Returns:
            bool: True if successful inserted, false otherwise 
        """
        data_to_insert = {}

        def check_user_exist():
            username = data['username']

            result = self.search_username(username)

            if result is not None:
                return result

        if not check_user_exist():
            for key, value in data.items():
                if key in self.permissive_keys_for_create_users:
                    data_to_insert[key] = value
                else:
                    pass
            self.db.insert(data_to_insert)
            return True

    def check_user_exist(self, username: str = '', email: str = ''):

        if not self.search_username(username):
            return self.search_email(email)
        else:
            return True

    # A class User need to be passed into the constructor

    def update_user(self, who, new_info):
        """ This two for loops verify if the info of new info is empty
            case true: delete the key, and update just the changed info
        """

        try:
            if self.check_user_exist(new_info['username'], new_info['email']):
                raise KeyError
        except KeyError:
            pass

        keys_to_delete = []

        for key, value in new_info.items():
            if not value:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del new_info[key]

        self.db.update(new_info, Query().email == who.email)

    def get_user_data(self, who):

        guest = {
            'username': 'guest',
            'password': 'erro',
            'email': 'erro',
            'store': '0',
            'level': 'guest',
            'when_was_created': 'erro',
        }

        # Try to get the user by username, if it is a empty dict then try to get by email
        try:
            by_username = self.db.search(Query().username == who.username)
            by_email = self.db.search(Query().email == who.email)
            if not by_username:
                return by_email[0]
            else:
                return by_username[0]

        # Dont need error thrating
        except:
            return guest

    def get_all_users(self):
        users = self.db.search(Query().username != '')
        new_users_protected = []

        # For security reasons the password is deleted before returning
        for user in users:
            del user['password']
            new_users_protected.append(user)

        return new_users_protected

    def get_users_by_search(self, search):
        users = self.get_all_users()

        filtered_users = []

        for user in users:
            if str(search).lower() in str(user['username']).lower():
                filtered_users.append(user)

        return filtered_users

    def get_users_by_store(self, store):
        users = self.get_all_users()

        filtered_users = []

        for user in users:
            if int(store) == user['store']:
                filtered_users.append(user)

        return filtered_users

    def insert_production(self, store, date, data):

        store_name = self.stores[store]

        default_day = {
            'big_ball': 0,
            'small_ball': 0,
            'garlic_bread': 0,
            'mozzarela': 0,
            'edamer': 0,


        }
        if self.get_day_production(store, date) == default_day:
            self.db.table(store_name).insert({'date': str(date),
                                              'production': data})

        else:

            old_data = self.get_day_production(store, date)

            self.update_production(
                store=store, date=date, old_data=old_data, new_data=data)

    def update_production(self, store, date, old_data, new_data):
        """_summary_

        Args:
            store (_type_): _description_
            date (_type_): _description_
            old_data (_type_): _description_
            new_data (_type_): _description_
        """
        store_name = self.stores[store]

        generated_data = {}

        for article_id, article_name in old_data.items():

            if new_data[article_id] == 0:
                generated_data[article_id] = old_data[article_id]
            else:
                generated_data[article_id] = old_data[article_id] + \
                    new_data[article_id]

        self.db.table(store_name).update(
            {'production': generated_data}, Query().date == str(date))

    def get_day_production(self, store, date):
        store_name = self.stores[int(store)]

        result = self.db.table(store_name).search(Query().date == str(date))

        try:
            return result[0]['production']

        except IndexError:

            return self.default_production

        except KeyError:
            return self.default_production

    def insert_consumes(self, who, date, store, data):

        store_name = self.stores[store]

        result = self.get_day_consume(store, date)

        if result:
            self.update_consume(who, date, store, result[0], data)
        else:
            self.db.table(store_name).insert({'date': date, who: data})

    def update_consume(self, who, date, store, old_data, new_data):
        store_name = self.stores[store]

        try:
            for key, value in old_data[who].items():
                new_data[key] += value
        except KeyError:
            pass

        self.db.table(store_name).update({who: new_data}, Query().date == date)

    def get_day_consume(self, store, date):

        store_name = self.stores[store]

        result = self.db.table(store_name).search((Query().date == date))

        if result:
            del result[0]['date']
        return result

    def insert_wasted(self, who, date, store, data):
        store_name = self.stores[store]

        result = self.db.table(store_name).search(
            Query().date == date)

        if result:
            try:
                if result[0][who]:
                    self.update_wasted(who, date, store, data)
            except:
                self.db.table(store_name).update(
                    result, {'date': date, who:  data})
        else:
            self.db.table(store_name).insert({'date': date, who: data})

    def update_wasted(self, who, date, store, data):
        store_name = self.stores[store]

        result = self.db.table(store_name).search(Query().date == date)[0]

        try:
            old_wasted = result[who]

            for key, value in old_wasted.items():
                if key in data:
                    data[key] += old_wasted[key]
                else:
                    data[key] = value

            self.db.table(store_name).update({'date': date, who: data})

        except:
            pass


if __name__ == '__main__':
    teste = DbConnection('databases/consumes.json')
    # print(teste.insert_wasted('Thawan', '2023', 3, {'bread': 5}))
    teste.insert_consumes('Thawan', '2023', 3, {'Laranja': 5})
