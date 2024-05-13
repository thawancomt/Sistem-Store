from flaskr.models import User
from flaskr.dbconnection import DbConnection
default_path = {'tasks': 'flaskr/databases/tasks.json'}
class Store():

    def __init__(self):
        self.store = 0
        self.workers = User().return_filtered_users_by_store(self.store)
        self.frizers = []
        self.tasks = {}

    def create_task(self, date, task, description = ''):
        return DbConnection(default_path.get('tasks')).create_task(date, self.store, task, description)

    def delete_task(self, date, task):
        return DbConnection(default_path.get('tasks')).delete_task(date, self.store, task)

    def task_concluded(self, date, task):
        return DbConnection(default_path.get('tasks')).put_task_as_concluded(date, self.store, task)

    def get_all_tasks(self, date):
        return DbConnection(default_path.get('tasks')).get_all_tasks(date, self.store)

    def get_concluded_tasks(self, date):
        return DbConnection(default_path.get('tasks')).get_all_tasks_concluded(date, self.store)
