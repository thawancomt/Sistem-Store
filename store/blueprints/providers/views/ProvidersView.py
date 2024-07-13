from flask import Blueprint, redirect, render_template, g, request

from ..services.ProvidersService import ProvidersService

providers = Blueprint('providers', __name__, template_folder='../templates',
                      static_folder='../static',
                      url_prefix='/providers')


@providers.route('/')
def home():
    provider_service = ProvidersService()
    
    context = {
        'active_providers': provider_service.get_active_providers()
    }
    return render_template('providers_home.html', context=context)

@providers.route('/create', methods=['POST'])
def create():
    data = request.form
    ProvidersService.create(data)
    
    return redirect(providers.url_prefix)