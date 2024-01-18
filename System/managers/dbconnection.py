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

        username = data['username']
        email = data['email']

        if not self.check_user_exist(username, email):
            for key, value in data.items():
                if key in self.permissive_keys_for_create_users:
                    data_to_insert[key] = value
                else:
                    pass
                
            self.db.insert(data_to_insert)
            return True

    def check_user_exist(self, username: str = '', email: str = ''):

        if not self.search_username(username):
            if self.search_email(email):
                return True
        else:
            return True

    # A class User need to be passed into the constructor

    def update_user(self, who, new_info):
        """ This two for loops verify if the info of new info is empty
            case true: delete the key, and update just the changed info
        """
        

        try:
            username = new_info['username']
            email = new_info['email']
            if self.check_user_exist(username, email):
                raise 'This User Already Exist'
        except:
            return False

        keys_to_delete = []

        for key, value in new_info.items():
            if not value:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del new_info[key]

        self.db.update(new_info, Query().email == who.email)

    def delete_user(self, email):
        print( self.db.remove(Query().email == email))

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
        for article, amount in data.items():

            if amount.isnumeric():
                print(amount.isnumeric(), amount)
                data[article] = int(amount)
            else:
                # If the amount is not numeric, return false
                return False

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
                generated_data[article_id] = int(old_data[article_id]) + int(new_data[article_id])

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

        # Convert the data to int
        for article, amount in data.items():
            if not article == 'who_consume':
                data[article] = int(amount)

        store_name = self.stores[store]

        result = self.get_day_consume(store, date)

        if data.get('who_consume'):
            del data['who_consume']

        if result:
            self.update_consume(who, date, store, data)
        else:
            self.db.table(store_name).insert({'date': date, who: data})

    def update_consume(self, who, date, store, new_data):

        store_name = self.stores[store]

        if new_data:

            old_data = self.get_day_consume(store, date).get(who, {})


            
            for article, amount in old_data.items():
                new_data[article] = int(new_data[article])
                new_data[article] += int(amount)

            self.db.table(store_name).update({who: new_data}, Query().date == date)

    def get_day_consume(self, store, date):

        store_name = self.stores[store]

        result = self.db.table(store_name).search((Query().date == date))

        # Delete the date key to return just the consume
        if result:
            # Check if the result has a date key
            if result[0].get('date'):
                del result[0]['date']
                
            return result[0]
        else:
            return {}

    def insert_wasted(self, who, date, store, data):
        store_name = self.stores[store]

        result = self.db.table(store_name).search(Query().date == date)

        # delete the who_consume key to send directly to the database
        del data['who_consume']

        if result:
            self.update_wasted(who, date, store, data)
        else:
            self.db.table(store_name).insert({'date': date, who: data})

    def update_wasted(self, who, date, store, data):
        store_name = self.stores[store]
        old_data = {}
        result = self.db.table(store_name).search(Query().date == date)

        new_data = data
        try:
            for key, value in old_data[who].items():
                new_data[key] += value
        except KeyError:
            pass

    def create_task(self, date, store, task, description = ''):

        if not description:
            description = 'Empty description'

        if not task:
            return False

        store_name = self.stores[int(store)]

        result = self.db.table(store_name).search(Query().date == date)

        if result:

            existent_tasks = result[0]['tasks']

            final_tasks = []

            
            if len(existent_tasks) > 0:
                
                for task_ in existent_tasks:
                    
                    for task_name, task_description in task_.items():

                        if task_name != task:

                            final_tasks.append({task_name : task_description})

                final_tasks.append({task: description})

                self.db.table(store_name).update(
                                    {'tasks':  final_tasks}, Query().date == date)       
            else:
                self.db.table(store_name).update(
                                    {'tasks':  [{task : description}]}, Query().date == date)

        else:
            self.db.table(store_name).insert(
                {'date': date, 'tasks': [{task : description}]})

    def delete_task(self, date, store, task_to_delete):

        store_name = self.stores[int(store)]

        result = self.db.table(store_name).search(Query().date == date)

        if result:

            tasks = result[0]['tasks']

            final_task = []

            for task in tasks:
                for task_name, task_description in task.items():
                    if task_name != task_to_delete:
                        final_task.append({task_name: task_description})


            self.db.table(store_name).update({'tasks' : final_task}, Query().date == date)

            

    def get_task_description(self, date, store, task_to_search):

        store_name = self.stores[int(store)]

        result = self.db.table(store_name).search(Query().date == date)

        if result:
            for task in result[0]['tasks']:
                for task_name, task_description in task.items():
                    if task_name == task_to_search:        
                        if task_description:
                            return task_description
        else:
            return False

    def put_task_as_concluded(self, date, store, task_to_put_as_concluded):
        store_name = self.stores[int(store)]
        
        # Get the tasks from the database based on the date provided
        result = self.db.table(store_name).search(Query().date == date)

        # Verify if task exitst in tasks:
        if not self.get_task_description(date, store, task_to_put_as_concluded):
            return False

        if result:
            # Get the concluded tasks
            concluded_tasks = result[0].get('concluded', [])
            
            # Get the task description
            task_description = self.get_task_description(date, store, task_to_put_as_concluded)

            # Set the new concluded task in a variable
            new_concluded_task = {task_to_put_as_concluded : task_description}

            # Append the new concluded task to the concluded tasks
            concluded_tasks.append(new_concluded_task)

            # Update the database
            self.db.table(store_name).update({'concluded' : concluded_tasks}, Query().date == date)

            # Delete the task from the tasks
            self.delete_task(date, store, task_to_put_as_concluded)
           
    def get_all_tasks(self, date, store):
        store_name = self.stores[int(store)]

        result = self.db.table(store_name).search(Query().date == date)

        if result:
            return result[0]['tasks']

    def get_all_tasks_concluded(self, date, store):
        store_name = self.stores[int(store)]

        result = self.db.table(store_name).search(Query().date == date)

        if result:
            try:
                concluded_tasks = result[0]['concluded']
                return concluded_tasks

            except KeyError:
                return []
        else:
            return []
    

if __name__ == '__main__':
    teste = DbConnection('System/databases/consumes.json')
    # print(teste.get_day_consume(5, '2024-01-18'))
    teste.insert_consumes('thawan2', '2024-01-18', 5, {'slices' : 2, 'bread' : -1})