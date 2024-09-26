from flask import Blueprint, redirect, render_template, g, request

from ..services.ProvidersService import ProvidersService

from flask_login import login_required, fresh_login_required

providers = Blueprint('providers', __name__, template_folder='../templates',
                      static_folder='../static',
                      url_prefix='/providers')

provider_service = ProvidersService()
@providers.route('/')
@login_required
def home():    
    context = {
        'active_providers': provider_service.get_active_providers()
    }
    return render_template('providers_home.html', context=context)

@providers.route('/create', methods=['POST'])
@fresh_login_required
def create():
    data = request.form
    ProvidersService.create(data)
    
    return redirect(providers.url_prefix)

@providers.route('/edit/<int:provider_id>', methods=['GET', 'POST'])
@fresh_login_required
def update(provider_id):
    context = {
        'provider' : provider_service.get(int(provider_id))
    }
    
    if request.method == 'POST':
        data = request.form
        provider_service.update(**data)
        return redirect(providers.url_prefix)
    return render_template('edit_provider.html', context=context)


@providers.route('/delete/<int:provider_id>', methods=['GET', 'POST'])
@fresh_login_required
def delete(provider_id):
    provider_service.delete(int(provider_id))
    return redirect(providers.url_prefix)

@providers.route('/activate/<int:provider_id>')
@fresh_login_required
def activate(provider_id):
    provider_service.activate(int(provider_id))
    return redirect(providers.url_prefix)


# make provider a class and use the class to create the blueprint
from store.utils import *
from store.extensions import BlueprintBase
class ProviderBlueprint():
    def __init__(self, name=None, static_folder=None, url_prefix=None, template_folder=None, import_name=None,) -> None:
        self.blueprint = Blueprint(name, import_name, url_prefix=url_prefix, template_folder=template_folder, static_folder=static_folder)
        self.register_routes()
        
    def register_routes(self):
        self.blueprint.add_url_rule('/', 'home', home, methods=['POST', 'GET'])
        self.blueprint.add_url_rule('/create', 'create', create, methods=['POST'])
        self.blueprint.add_url_rule('/edit/<int:provider_id>', 'update', update, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/delete/<int:provider_id>', 'delete', delete, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/activate/<int:provider_id>', 'activate', activate)
        
    def update(self):
        pass

    def create(self):
        data = request.form
        ProvidersService.create(data)
    
        return redirect(providers.url_prefix)
    def delete(self):
        pass
    