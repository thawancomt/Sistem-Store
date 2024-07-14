from flask import Blueprint, redirect, render_template, g, request

from ..services.ProvidersService import ProvidersService

providers = Blueprint('providers', __name__, template_folder='../templates',
                      static_folder='../static',
                      url_prefix='/providers')

provider_service = ProvidersService()
@providers.route('/')
def home():    
    context = {
        'active_providers': provider_service.get_active_providers()
    }
    return render_template('providers_home.html', context=context)

@providers.route('/create', methods=['POST'])
def create():
    data = request.form
    ProvidersService.create(data)
    
    return redirect(providers.url_prefix)


@providers.route('/edit/<int:provider_id>', methods=['GET', 'POST'])
def update(provider_id):
    context = {
        'provider' : provider_service.get(int(provider_id))
    }
    
    if request.method == 'POST':
        data = request.form
        provider_service.update(**data)
        return redirect(providers.url_prefix)
    return render_template('edit_provider.html', context=context)
