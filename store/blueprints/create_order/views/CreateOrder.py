from store.utils import *
from store.extensions import BlueprintBase

from ...articles.services.ArticlesService import ArticlesService

class CreateOrderBlueprint(BlueprintBase):
    def __init__(self, name='orders', import_name=__name__,
                 template_folder='../templates',
                 url_prefix='/orders',
                 static_folder='../static'):
        
        self.blueprint = Blueprint(name, import_name,
                                   template_folder=template_folder,
                                static_folder=static_folder,
                                url_prefix=url_prefix)
        
        self.register_routes()

    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index)

    def index(self):
        context = {
            'articles' : ArticlesService().get_all_active()
        }
        return render_template('index.html', context = context)
    def create(self):
        pass
    def update(self):
        pass
    def delete(self):
        pass

CreateOrderBlueprint = CreateOrderBlueprint().blueprint