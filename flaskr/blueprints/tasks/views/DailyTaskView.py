from flask import Blueprint, render_template, request, redirect, url_for

from flask_login import login_required

from ..services.DailyTaskService import DailyTaskService, DailyTaskStatusService

#python buildin
from datetime import datetime


daily_task = Blueprint('daily_task', __name__,
                       template_folder='../templates',
                       url_prefix='/daily')
@daily_task.route('/')
@login_required
def view_daily_tasks():
    date = request.args.get('date', None) or datetime.now().strftime('%Y-%m-%d')



    daily_tasks = DailyTaskService().get_all()
    daily_tasks_to_do = DailyTaskStatusService(date=date).get_all()
    
    context = {
        'all_tasks' : daily_tasks,
        'to_do' : daily_tasks_to_do,
        'date' : date
    }
    
    return render_template('daily_task.html', context=context)

@daily_task.route('/create', methods=['POST'])
@login_required
def create():
    name = request.form.get('name', None)
    description = request.form.get('description', None)
    
    DailyTaskService(name=name, description=description).create()
    
    return redirect(url_for('tasks.daily_task.view_daily_tasks'))
    
    pass

@daily_task.route('/finish', methods=['POST'])
@login_required
def set_task_as_done():
    data = request.form.to_dict()
    
    date = request.args.get('date', None) or datetime.now().strftime('%Y-%m-%d')

    DailyTaskStatusService(date=date).set_as_done(data=data)
    
    
    
    return redirect(url_for('tasks.daily_task.view_daily_tasks', date=date))