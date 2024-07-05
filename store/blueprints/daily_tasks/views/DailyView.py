from  flask import Blueprint, render_template, request, redirect, g, url_for


from ..services.DailyTasksService import DailyTasksService
from ..services.DailyTasksStatusService import DailyStatusService, datetime

from flask_login import fresh_login_required, login_required


daily_tasks = Blueprint('daily_tasks', __name__,
                        template_folder='../templates',
                        static_folder='../static',
                        url_prefix='/daily_tasks')

@daily_tasks.route('/')
def index():
    context = {
        'active_daily_tasks' : DailyTasksService().get_all_active_tasks(),
        'to_do' : DailyStatusService(date=g.date).get_all_tasks(),
    }
    
    return render_template('daily_tasks.html', context = context)

@daily_tasks.route('/create', methods=['POST'])
@fresh_login_required
def create():
    data = request.form.to_dict()
    DailyTasksService().create_task(data)
    return redirect('/daily_tasks')

# Create the set as done method
@daily_tasks.route('/finish', methods=['POST'])
@login_required
def set_as_done():
    data = request.form.to_dict()
    
    day_status = DailyStatusService(date=g.date)
    day_status.update_day_status(data)
    
    return redirect(url_for('daily_tasks.index', date=g.date))

@daily_tasks.route('/deactive', methods=['POST'])
@fresh_login_required
def deactive_task():
    task_id = request.form.get('task_id')
    date = request.args.get('date', g.date)
    DailyTasksService(date=date).deactive_task(task_id)
    return redirect('/daily_tasks')

@daily_tasks.route('/edit', methods=['GET'])
@login_required
def edit_view():
    task_id = request.args.get('task_id')
    
    task = DailyTasksService().get_task_by_id(int(task_id))
    
    context = {
        'task' : task,
    }   
    
    return render_template('edit_daily_task.html', context=context)

@daily_tasks.route('/edit', methods=['POST'])
@login_required
def edit_task():
    data = request.form.to_dict()
    
    if 'status' in data:
        data['status'] = True
    
    DailyTasksService(data.get('task_id')).update_task(data)
    
    return redirect(url_for('daily_tasks.index'))


