from users import User


class Store():

    def __init__(self, store):
        self.store = int
        self.workers = User().return_filtered_users_by_store(store)
        self.frizers = []
        self.tasks = {}

    def open_task(self):
        self.tasks['open_tasks'] = ['turn on the light', 'turn on the oven']


teste = Store(5)

print(teste.workers)
