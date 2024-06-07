from flask import Blueprint, render_template, request, redirect, url_for

from flask_login import login_required

from ..services.DailyTaskService import DailyTaskService

daily_task = Blueprint('daily_task', __name__,
                       template_folder='../templates',
                       url_prefix='/daily')
@daily_task.route('/')
@login_required
def view_daily_tasks():
    daily_tasks = DailyTaskService.get_all()
    
    context = {
        'all_tasks' : daily_tasks
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