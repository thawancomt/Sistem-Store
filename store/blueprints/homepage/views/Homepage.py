from store.utils import *
from store.extensions import BlueprintBase
from datetime import datetime



homepage = Blueprint('homepage', __name__,
                     url_prefix='/homepage',
                     template_folder='../templates',
                     static_folder= '../static')


from store.blueprints.tasks.services.TaskService import TaskService
from store.blueprints.stores_management.services.StoreService import StoreService
from flask_login import login_required, current_user, fresh_login_required

import os



@homepage.route('/', methods=['GET', 'POST'])
@fresh_login_required
def home():

    context = {
        'tasks' : {
            'all_tasks' : TaskService.get_tasks_of_day(),
            'active_tasks' : TaskService.get_active_tasks_of_day(),
            'done_tasks' : TaskService.get_done_tasks_of_day(),
        },
        'date' : datetime.now().strftime('%d/%m/%Y'),
        'store_name' : StoreService().get_name_by_id(current_user.store_id)
    }

    
    return render_template('homepage.html', context=context, os=os)


class HomepageBluprint(BlueprintBase):
    def __init__(self, name=None, static_folder=None, url_prefix=None, template_folder=None, import_name=None,) -> None:
        super().__init__(name, static_folder, url_prefix, template_folder, import_name)
        self.register_routes()
        

        
    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index, methods=['POST', 'GET'])
    def update(self):
        return super().update()
    def create(self):
        return super().create()
    def delete(self):
        return super().delete()
    
    @login_required
    def index(self):
        context = {
            'tasks' : {
                'all_tasks' : TaskService.get_tasks_of_day(),
                'active_tasks' : TaskService.get_active_tasks_of_day(),
                'done_tasks' : TaskService.get_done_tasks_of_day(),
            },
            'date' : datetime.now().strftime('%d/%m/%Y'),
            'store_name' : StoreService().get_name_by_id(current_user.store_id)
            }

    
        return render_template('homepage.html', **context)
    
HomepageBluprint = HomepageBluprint('homepage', url_prefix='/index', template_folder='../templates', static_folder= '../static', import_name=__name__).blueprint