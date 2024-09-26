from store.extensions import *

from ..Services.ShelLifeService import ShelLifeService
from store.utils import *

class ShelfLifeBlueprint(BlueprintBase):
    def __init__(self, name=None, static_folder=None, url_prefix=None, template_folder=None, import_name=None,) -> None:
        super().__init__(name, static_folder, url_prefix, template_folder, import_name)
        self.register_routes()

    def register_routes(self):
        self.blueprint.add_url_rule('/', 'home', self.index, methods=['GET'])

    def index(self):
        context = {
            'alerts' : ShelLifeService().get_by_date()
        }
        return render_template('shelf_life_home.html', **context)
    
    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass



ShelfLifeBlueprint = ShelfLifeBlueprint(name='shelflife', url_prefix='/shelf_life', template_folder='../templates', static_folder='../static', import_name=__name__).blueprint
