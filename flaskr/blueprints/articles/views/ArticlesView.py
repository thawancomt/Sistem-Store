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
                     url_prefix='/articles')

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
    name = request.form.get('name')
    description = request.form.get('description')
    type_unit = request.form.get('type_unit')
    is_producible = bool(request.form.get('is_producible'))

    
    article = ArticlesService(name=name, description=description, type_unit=type_unit, is_producible = is_producible)
    
    article.create()
    return redirect(url_for('articles.view'))

