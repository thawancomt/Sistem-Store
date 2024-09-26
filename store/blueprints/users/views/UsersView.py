from store.utils import *
from store.extensions import *
from .EditUserView import edit_user
from .CreateUserView import create_user

from store.blueprints.users.services.UserService import UserService


class UsersBlueprint(BlueprintBase):
    def __init__(self, name=None, static_folder=None, url_prefix=None, template_folder=None, import_name=None,) -> None:
        super().__init__(name, static_folder, url_prefix, template_folder, import_name)
        self.register_routes()

    def register_routes(self):
        self.blueprint.add_url_rule('/', view_func=self.index, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/table', view_func=self.users_table)

        
        self.blueprint.register_blueprint(edit_user)
        self.blueprint.register_blueprint(create_user)
    
    def index(self):
        # Stand by home
        user_query = request.form.get('user_query', None)
        context = {
            'all_users': UserService.get_all_active_users(query=user_query),
            'inactive_users': UserService.get_all_inactive_users(query=user_query)
        }

        return render_template('users.html', context=context)
    
    def users_table(self):
        users = UserService().get_all()
        
        context = {
            'all_users': users
        }

        return render_template('users_table.html', context=context)

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

UsersBlueprint = UsersBlueprint('users', url_prefix='/users', template_folder='../templates', static_folder= '../static', import_name=__name__).blueprint