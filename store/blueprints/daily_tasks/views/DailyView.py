from store.utils import *
from store.extensions import BlueprintBase, login_required, fresh_login_required


from ..services.DailyTasksService import DailyTasksService
from ..services.DailyTasksStatusService import DailyStatusService, datetime


class DailyTasksBlueprint(BlueprintBase):
    def __init__(self, name='daily_tasks', import_name=__name__,
                 template_folder='../templates',
                 url_prefix='/daily_tasks',
                 static_folder='../static'):
        
        self.blueprint = Blueprint(name, import_name,
                                template_folder=template_folder,
                                static_folder=static_folder,
                                url_prefix=url_prefix)
        self.register_routes()
    
    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index)
        self.blueprint.add_url_rule('/create', 'create', self.create)
        self.blueprint.add_url_rule('/set_as_done', 'set_as_done', self.set_as_done, methods=['POST'])
        self.blueprint.add_url_rule('/deactive', 'deactive_task', self.deactive_task, methods=['POST'])
        self.blueprint.add_url_rule('/edit', 'edit_view', self.edit_view, methods=['post', 'get'])
        self.blueprint.add_url_rule('/update', 'update', self.update, methods=['post'])

    def index(self):
        context = {
            'active_daily_tasks' : DailyTasksService().get_all_active_tasks(),
            'to_do' : DailyStatusService(date=g.date).get_all_tasks(),
        }
        
        return render_template('daily_tasks.html', context = context)


    @fresh_login_required
    def create(self):
        data = request.form.to_dict()
        DailyTasksService().create_task(data)
        return redirect('/daily_tasks')


    @login_required
    def set_as_done(self):
        data = request.form.to_dict()
        
        day_status = DailyStatusService(date=g.date)
        day_status.update_day_status(data)
        
        return redirect(url_for('daily_tasks.index', date=g.date))

    @fresh_login_required
    def deactive_task(self):
        task_id = request.form.get('task_id')
        date = request.args.get('date', g.date)
        DailyTasksService(date=date).deactive_task(task_id)
        return redirect('/daily_tasks')

    @login_required
    def edit_view(self):
        task_id = request.args.get('task_id')
        
        task = DailyTasksService().get_task_by_id(int(task_id))
        
        context = {
            'task' : task,
        }
            
        
        return render_template('edit_daily_task.html', context=context)

    def update(self):
        data = request.form.to_dict()
    
        if 'status' in data:
            data['status'] = True
        
        DailyTasksService(id=data.get('task_id')).update_task(data)
        
        return redirect(url_for('daily_tasks.index'))

    @login_required
    def edit_task(self):
        pass

    def delete(self):
        pass

DailyTasksBlueprint = DailyTasksBlueprint().blueprint
        
