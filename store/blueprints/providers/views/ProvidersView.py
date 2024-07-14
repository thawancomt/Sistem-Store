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
