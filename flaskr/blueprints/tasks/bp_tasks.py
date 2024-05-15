from flaskr.blueprints import *

from flaskr.models.stores_management import Store


tasks_bp = Blueprint('tasks_bp', __name__,
                     url_prefix='/tasks')


@tasks_bp.route('/create', methods=['POST'])
def create_task(date_for = None, store_to_send = None):
    
    if date_for is None:
        date_for = datetime.now().strftime('%y-%m-%d')
    
    store = Store()
    store.store = store_to_send if store_to_send else 5
    
    data = request.form.to_dict()
    
    task_data = {
        'task_name' : data.get('task_to_send'),
        'task_description' : data.get('task_description')
    }
    
    store.create_task(date_for, task_data['task_name'], task_data['task_description'])

    return redirect(url_for('home_bp.home'))