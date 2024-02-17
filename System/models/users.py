from tinydb import Query
from .dbconnection import DbConnection
from hashlib import sha256

default_path = {'users' : 'System/databases/users.json'}

class User(DbConnection):
    permissive_keys = ['username', 'password',
                       'level', 'email', 'store', 'last_login']
    levels_of_users = [
        'admin',
        'worker',
        'guest'
    ]

    def __init__(self):
        self.username = ''
        self.password = ''
        self.email = ''
        self.store = None
        self.last_login = None
        self.level = None
        self.when_was_created = None
        super().__init__(default_path.get('users'))

    def get_user_data(self, who):
        result = DbConnection(default_path.get('users')).get_user_data(who)
        return result

    def edit_user(self, who, new_data):
        DbConnection(default_path.get('users')).update_user(who, new_data)

    def return_all_users(self):
        return DbConnection(default_path.get('users')).get_all_users()

    def return_filtered_users(self, search):
        return DbConnection(default_path.get('users')).get_users_by_search(search)

    def return_filtered_users_by_store(self, store):
        return DbConnection(default_path.get('users')).get_users_by_store(int(store))

    def delete_user(self, who):
        store = User().get_user_data(who)['store']
        email = who.email
        
        return DbConnection(default_path.get('users')).delete_user(store, email)
        
        
class CreateUser():
    def __init__(self, who):

        self.data = {
            'username': who.username,
            'password': sha256(who.password.encode()).hexdigest(),
            'email': who.email,
            'store': who.store,
            'level': who.level,
            'last_login': who.last_login,
            'when_created': who.when_was_created,
        }


    def create_user(self):
        if DbConnection(default_path.get('users')).insert_user(self.data):
            return True
        else:
            return False


class Login(DbConnection):

    def __init__(self, who, db=default_path.get('users')):
        super().__init__(db)
        self.email = who.email
        self.password = who.password

    @property
    def password(self):
        return sha256(self._password.encode()).hexdigest()
    
    @password.setter
    def password(self, value):
        self._password = value

    def validate(self):
        for table in self.db.tables():
            if self.db.table(table).search((Query().email == self.email) &
                            (Query().password == self.password)):
                return True
        else:
            return False


class Session(DbConnection):
    connected_users = {}

    def __init__(self, adress=None, who=None):

        super().__init__(default_path.get('users'))

        self.adress = adress
        self.who = who
        self.status = False

    def connect_user(self):

        needed_data = self.get_user_data(self.who)

        self.connected_users[self.adress] = {
            'username':  needed_data['username'],
            'email':  needed_data['email'],
            'store': needed_data['store'],
            'status': self.status,
            'level': needed_data['level']
        }

    def disconnect_user(self):
        self.connected_users[self.adress] = self.get_user_data(self.who)

    def get_session(self):
        try:
            return self.connected_users[self.adress]
        except:
            Session(self.adress).connect_user()
            return self.connected_users[self.adress]

    # Get info methods
    def name(self):
        return self.get_session()['username']

    def level(self):
        return self.get_session()['level']

    def store_name(self, id=False):
        if not id:
            return DbConnection.stores.get(self.get_session()['store'])
        else:
            return self.get_session()['store']
