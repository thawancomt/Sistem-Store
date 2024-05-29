from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..services.ProductionService import ProductionService
from ...articles.services.ArticlesService import ArticlesService

production = Blueprint('production', __name__, url_prefix='/production',
                       template_folder='../templates')

@production.route('/')
def home():
    context = {
        'productions' : ProductionService.get_all(),
        'articles' : ArticlesService.get_all()
    }
    return render_template('production.html', context=context)