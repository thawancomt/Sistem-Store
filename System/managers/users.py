from tinydb import Query

if __name__ == '__main__':
    from dbconnection import DbConnection
else:
    from managers.dbconnection import DbConnection


class User():
    permissive_keys = ['username', 'password', 'level', 'email', 'store']

    def __init__(self):
        self.username = ''
        self.password = ''
        self.email = ''
        self.store = None
        self.last_login = None
        self.level = None
        self.when_was_created = None

    def get_user_data(self, who):
        result = DbConnection('teste.json').get_user_data(who)
        return result

    def edit_user(self, who, new_data):
        DbConnection('teste.json').update_user(who, new_data)


class CreateUser(User):
    def __init__(self, who):

        super().__init__()

        data = {
            'username': who.username,
            'password': who.password,
            'email': who.email,
            'store': who.store,
            'level': who.level,
            'when_was_created': who.when_was_created,
        }

        DbConnection('teste.json').insert_user(data)


class Login(DbConnection):

    def __init__(self, who, db='teste.json'):
        super().__init__(db)
        self.email = who.email
        self.password = who.password

    def validate(self):
        if self.db.search((Query().email == self.email) &
                          (Query().password == self.password)):
            return True
        else:

            print("Invalid username or password")
            return False


class Session(DbConnection):
    connected_users = {}

    def __init__(self, adress=None, who=None):

        super().__init__('teste.json')

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
            return DbConnection.stores[self.get_session()['store']]
        else:
            return self.get_session()['store']
