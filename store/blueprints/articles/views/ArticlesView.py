from store.utils import *
from store.extensions import login_required, fresh_login_required

from ..services.ArticlesService import ArticlesService, TypeUnitsService
from ...providers.services.ProvidersService import ProvidersService

# type unit Blueprint 

# type_unit = Blueprint('type_unit', __name__, 
#                      template_folder='../templates',
#                      url_prefix='/type_unit')
# 
# @type_unit.route('/')
# def index():
#     context = {
#         'type_units': TypeUnitsService.get_all()
#     }
#     return render_template('type_unit.html', context=context)
# 
# @type_unit.route('/create', methods=['POST'])
# def insert():
#     name = request.form.get('name')
#     description = request.form.get('description')
#     alias = request.form.get('alias')
#     
# 
#     type_unit = TypeUnitsService(name=name, description=description, alias=alias)
#     type_unit.create()
#     return redirect(url_for('articles.type_unit.index'))


# Article blueprint

articles = Blueprint('articles', __name__, 
                     template_folder='../templates',
                     url_prefix='/articles',
                     static_folder='../static')


@articles.get('/')
@login_required
def index():
    
    context = {
        'articles': ArticlesService.get_all(),
        'type_units': TypeUnitsService.get_all(),
        'providers' : ProvidersService.get_active_providers()
    }
    return render_template('Articles.html', context=context)


@articles.post('/create')
@login_required
def create():
    
    ArticlesService().create(
        request.form.to_dict()
    )
    
    return redirect(url_for('articles.index'))


@articles.get('/update/<int:article_id>')
@login_required
def update_view(article_id):
    
    article = ArticlesService().get_by_id(article_id)
    types = TypeUnitsService.get_all()

    context = {
        'article' : article,
        'types' : types
    }

    return render_template('UpdateArticle.html', context = context)

@articles.post('/update/<int:article_id>')
@fresh_login_required
def update(article_id):
    data = request.form.to_dict()
    ArticlesService().update(data)
    return redirect(url_for('articles.index'))

@articles.post('/delete/<int:article_id>')
@fresh_login_required
def delete(article_id):
    ArticlesService().delete(article_id)
    return redirect(url_for('articles.index'))

class ArticlesBlueprint():
    def __init__(self, name='articles', import_name=__name__,
                 template_folder='../templates',
                 url_prefix='/articles',
                 static_folder='../static'):
        
        self.blueprint = Blueprint(name, import_name,
                                   template_folder=template_folder,
                                static_folder=static_folder,
                                url_prefix=url_prefix)

        self.register_routes()
    
    def register_routes(self):
        self.blueprint.add_url_rule('/', 'index', self.index)