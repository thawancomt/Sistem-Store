from store.utils import *
from store.extensions import login_required, fresh_login_required, BlueprintBase


from ..services.ArticlesService import ArticlesService, TypeUnitsService
from ...providers.services.ProvidersService import ProvidersService

class TypeUnitBlueprint:
    def __init__(self, name='type_unit', import_name=__name__,
                 template_folder='../templates',
                 url_prefix='/type_unit',
                 static_folder='../static'):
        
        self.blueprint = Blueprint(name, import_name,
                                   template_folder=template_folder,
                                static_folder=static_folder,
                                url_prefix=url_prefix)
        
        self.register_routes()
    
    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.blueprint.add_url_rule('/create', 'create', self.create, methods=['POST'])
    
    def index(self):
        context = {
            'type_units': TypeUnitsService.get_all()
        }

        return render_template('TypeUnit.html', context=context)
    
    def create(self):
        name = request.form.get('name')
        description = request.form.get('description')
        alias = request.form.get('alias')


        type_unit = TypeUnitsService(name=name, description=description, alias=alias)
        type_unit.create()
        return redirect(url_for('articles.type_unit.index'))
        

        


class ArticlesBlueprint(BlueprintBase):
    def __init__(self, name='articles', import_name=__name__,
                 template_folder='../templates',
                 url_prefix='/articles',
                 static_folder='../static'):
        
        self.blueprint = Blueprint(name, import_name,
                                   template_folder=template_folder,
                                static_folder=static_folder,
                                url_prefix=url_prefix)
        
        self.blueprint.register_blueprint(TypeUnitBlueprint().blueprint)

        self.register_routes()
    
    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index)
        self.blueprint.add_url_rule('/update/<int:article_id>', 'update_view', self.update_view, methods=['GET'])
        self.blueprint.add_url_rule('/update/<int:article_id>', 'update', self.update, methods=['POST'])
        self.blueprint.add_url_rule('/create', 'create', self.create, methods=['POST'])
        self.blueprint.add_url_rule('/delete/<int:article_id>', 'delete', self.delete, methods=['POST'])
    
    @login_required
    def index(self):
        context = {
            'articles': ArticlesService.get_all(),
            'type_units': TypeUnitsService.get_all(),
            'providers': ProvidersService.get_active_providers()
        }
        return render_template('Articles.html', context=context)

    @login_required
    def create(self, ):
        
        ArticlesService().create(
            request.form.to_dict()
        )
        
        return redirect(url_for('articles.index'))


    @login_required
    def update_view(self, article_id):
        
        article = ArticlesService().get_by_id(article_id)
        types = TypeUnitsService.get_all()

        context = {
            'article' : article,
            'types' : types
        }

        return render_template('UpdateArticle.html', context = context)

    @fresh_login_required
    def update(self, article_id):
        data = request.form.to_dict()
        ArticlesService().update(data)
        return redirect(url_for('articles.index'))

    @fresh_login_required
    def delete(self, article_id):
        ArticlesService().delete(article_id)
        return redirect(url_for('articles.index'))
    

articles = ArticlesBlueprint().blueprint
type_unit = TypeUnitBlueprint().blueprint