from managers.users import User

from managers.dbconnection import DbConnection


class Store():

    def __init__(self):
        self.store = 0
        self.workers = User().return_filtered_users_by_store(self.store)
        self.frizers = []
        self.tasks = {}

    def create_task(self, date, task):
        return DbConnection('databases/tasks.json').create_task(date, self.store, task)

    def delete_task(self, date, task):
        return DbConnection('databases/tasks.json').delete_task(date, self.store, task)

    def task_concluded(self, date, task):
        return DbConnection('databases/tasks.json').put_task_as_concluded(date, self.store, task)

    def get_all_tasks(self, date):
        return DbConnection('databases/tasks.json').get_all_tasks(date, self.store)

    def get_concluded_tasks(self, date):
        return DbConnection('databases/tasks.json').get_all_tasks_concluded(date, self.store)
