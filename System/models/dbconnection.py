from tinydb import TinyDB, Query
from tinydb.operations import increment

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
        self.tables = self.db.tables()


    # Get functions
    @staticmethod
    def get_store_name(store_id : int) -> str:
        """Get the store name based on the dict of store's ID"""
        return DbConnection.stores.get(int(store_id))
    
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

    def get_all_tasks(self, date, store):
        store_name = DbConnection.get_store_name(store)

        result = self.db.table(store_name).search(Query().date == date)

        return result[0]['tasks'] if result else []

    def get_all_tasks_concluded(self, date, store):
        store_name = DbConnection.get_store_name(store)

        result = self.db.table(store_name).search(Query().date == date)

        if result:
            try:
                concluded_tasks = result[0]['concluded']
                return concluded_tasks

            except KeyError:
                return []
        else:
            return []
        

    # def get_task_description(self, date, store, task_to_search):
    #
    #    store_name = DbConnection.get_store_name(store)
    #
    #    result = self.db.table(store_name).search(Query().date == date)
    #
    #
    #    if result:
    #        tasks = result[0].get('tasks')
    #
    #    if tasks: 
    #        task_description = tasks.get(task_to_search)
    #        return task_description.get('text')
    #
    #    return False
        
    def get_day_consume(self, store, date):

        store_name = DbConnection.get_store_name(store)

        result = self.db.table(store_name).search((Query().date == date))

        if result:
            if result[0].get('date'):
                del result[0]['date']

            return result[0]
        else:
            return {}
        

    def get_wasted(self, store, date):
        store_name = DbConnection.get_store_name(store)

        result = self.db.table(store_name).search(Query().date == date)

        if result:
            return result[0]
        return {}
    

    def get_day_production(self, store, date):
        store_name = self.stores[int(store)]

        result = self.db.table(store_name).search(Query().date == str(date))

        try:
            return result[0]['production']

        except IndexError:

            return self.default_production

        except KeyError:
            return self.default_production

    # Insert functions
    def insert_user(self, data):
        """Insert a new user into the database

        Args:
            data dict: User data need be a dict

        Returns:
            bool: True if successful inserted, false otherwise
        """
        store_name = self.stores[data['store']]
        data_to_insert = {}

        username = data['username']
        email = data['email']

        if not self.check_user_exist(username, email):
            for key, value in data.items():
                if key in self.permissive_keys_for_create_users:
                    data_to_insert[key] = value
                else:
                    pass

            self.db.table(store_name).insert(data_to_insert)
            return True
        else:
            return False
        
    def insert_stock(self, data):
        self.db = TinyDB('System/databases/stock.json', indent=4)

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



        store_name = self.stores[store]

        result = self.get_wasted(store, date)

        # delete the who_consume key to send directly to the database
        if data.get('who_consume'):
            del data['who_consume']

        if result:
            self.update_wasted(who, date, store, data)
        else:
            self.db.table(store_name).insert({'date': date, who: data})

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
                amount = int(amount)
                data[article] = amount
            else:
                try:
                    data[article] = int(amount)
                except:
                    return False


        if self.get_day_production(store, date) == default_day:
            self.db.table(store_name).insert({'date': str(date),
                                              'production': data})

        else:

            old_data = self.get_day_production(store, date)

            self.update_production(
                store=store, date=date, old_data=old_data, new_data=data)


    def check_user_exist(self, username: str = '', email: str = ''):

        return True if self.search_username(username) or self.search_email(email) else False

    # Update functions
    def update_user(self, who, new_info):

        try:
            username = new_info['username']
            email = new_info['email']
            storeID = self.get_user_data(who)['store']
            store_name = self.stores[storeID]
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

        self.db.table(store_name).update(new_info, Query().email == who.email)
    
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
            {'production': generated_data}, Query().date == str(date)
        )

    

    
    def update_consume(self, who, date, store, new_data):

        store_name = self.stores[store]

        if new_data:

            old_data = self.get_day_consume(store, date).get(who, {})



            for article, amount in old_data.items():
                new_data[article] += int(amount)

            self.db.table(store_name).update({who: new_data}, Query().date == date)

    
    def update_wasted(self, who, date, store, data):

        store_name = self.stores[store]

        if data:
            old_data = self.get_wasted(store, date).get(who, {})

            for article, amount in old_data.items():
                data[article] += int(amount)

            self.db.table(store_name).update({who: data}, Query().date == date)



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

        store_name = self.stores[store]

        return self.db.table(store_name).remove(Query().email == email)
