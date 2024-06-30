from flask import Blueprint, render_template, request, redirect, url_for
from ..services.ArticlesService import ArticlesService, TypeUnitsService


type_unit = Blueprint('type_unit', __name__, 
                     template_folder='../templates',
                     url_prefix='/type_unit')

@type_unit.route('/')
def view():
    context = {
        'type_units': TypeUnitsService.get_all()
    }
    return render_template('type_unit.html', context=context)

@type_unit.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    description = request.form.get('description')
    alias = request.form.get('alias')
    

    type_unit = TypeUnitsService(name=name, description=description, alias=alias)
    type_unit.create()
    return redirect(url_for('articles.type_unit.view'))

articles = Blueprint('articles', __name__, 
                     template_folder='../templates',
                     url_prefix='/articles',
                     static_folder='../static')

articles.register_blueprint(type_unit)


@articles.route('/')
def view():
    context = {
        'articles': ArticlesService.get_all(),
        'type_units': TypeUnitsService.get_all()
    }
    return render_template('articles.html', context=context)


@articles.route('/create', methods=['POST'])
def create():
    data = request.form.to_dict()
    
        
    article = ArticlesService().create(data)
    return redirect(url_for('articles.view'))


@articles.route('/edit/<int:article_id>')
def edit_view(article_id):
    article = ArticlesService().get_by_id(article_id)
    types = TypeUnitsService.get_all()

    return render_template('edit_article.html', article_id=article_id, article=article, types=types)

@articles.route('/edit/<int:article_id>', methods=['POST'])
def edit(article_id):
    data = request.form.to_dict()
    

    article = ArticlesService().edit_article(data)

    return redirect(url_for('articles.view'))

@articles.route('/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    ArticlesService().delete(article_id)
    return redirect(url_for('articles.view'))

