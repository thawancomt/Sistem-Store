from  flask import Blueprint, render_template, request, redirect, g, url_for


from ..services.DailyTasksService import DailyTasksService
from ..services.DailyTasksStatusService import DailyStatusService, datetime

daily_tasks = Blueprint('daily_tasks', __name__,
                        template_folder='../templates',
                        url_prefix='/daily_tasks')

@daily_tasks.route('/')
def index():


    context = {
        'active_daily_tasks' : DailyTasksService().get_all_active_tasks(),
        'to_do' : DailyStatusService(date=g.date).get_all_tasks(),
    }
    
    return render_template('daily_tasks.html', context = context)

@daily_tasks.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    
    DailyTasksService().create_task(data)
    return redirect('/daily_tasks')

# Create the set as done method
@daily_tasks.route('/finish', methods=['POST'])
def set_as_done():
    data = request.form.to_dict()
    
    day_status = DailyStatusService(date=g.date)
    day_status.update_day_status(data)
    
    return redirect(url_for('daily_tasks.index', date=g.date))

@daily_tasks.route('/', methods=['POST'])
def deactive_task():
    task_id = request.form.get('task_id')
    date = request.args.get('date', g.date)
    
    DailyTasksService(date=date).deactive_task(task_id)
    return redirect('/daily_tasks')
