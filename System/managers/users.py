from tinydb import TinyDB, Query


class User():
    def __init__(self):
        self.username = ''
        self.password = ''
        self.email = ''
        self.store = None
        self.last_login = None
        self.admin = None
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
            'when_was_created': who.when_was_created,
        }

        DbConnection('teste.json').insert_user(data)


class DbConnection():
    def __init__(self, db):
        self.db = TinyDB(db, indent=4)

    def search_username(self, username):
        result = self.db.search(Query().username == username)
        return result

    def insert_user(self, data):

        def check_user_exist():
            username = data['username']

            result = self.search_username(username)

            if result is not None:
                return result

        if not check_user_exist():
            self.db.insert(data)

    def update_user(self, who, new_info):
        # If user wants to edit just one info, Ex: update just the name
        try:
            old_info = self.search_username(who.username)[0]

        except IndexError:
            raise 'UserNotFound'

        edited_user = User()

        edited_user.username = new_info['username']
        edited_user.email = new_info['email']
        edited_user.store = new_info['store']

        if new_info['username'] == '':

            edited_user.username = old_info['username']

        if new_info['email'] == '':

            edited_user.email = old_info['email']

        if new_info['store'] == '':

            edited_user.store = old_info['store']

        print(old_info)

        self.db.update({
            'username': edited_user.username,
            'email': edited_user.email,
            'store': edited_user.store,
            'when_was_created': old_info['when_was_created']}, Query().username == who.username)

    def get_user_data(self, who):
        result = self.db.search(Query().username == who.username)
        return result


class Login(DbConnection):

    def __init__(self, who, db='teste.json'):
        super().__init__(db)
        self.email = who.email
        self.password = who.password

    def validate(self):
        if self.db.search((Query().email == self.email) &
                          (Query().password == self.password)):
            print("Please enter")
            return True
        else:
            print("Invalid username or password")
            return False


thawan = User()
thawan.username = 'Thawan Henrdique'
thawan.password = 'teste'

print(bool(Login(thawan).validate()))


# DbConnection('teste.json').update_user(thawan, {'username': 'Vagabundo'})
