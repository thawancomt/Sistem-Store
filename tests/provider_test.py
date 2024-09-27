from tests.utils import app, client, db
from tests.login_test import login

from store.blueprints.articles.models.ProviderModel import ProviderModel as Provider
from store.blueprints.providers.services.ProvidersService import ProvidersService

from flask_sqlalchemy import SQLAlchemy
from flask.testing import FlaskClient
import pytest

app = app
client : FlaskClient = client
db : SQLAlchemy = db

def test_create_provider_service(client, db):
    login(client)
    
    data = {
        'name': 'Test Provider',
        'address' : 'Test Address',
        'active': True,
        'phone': '1234567890',
        'email': 'test@gmail.com'
    }

    with client.application.app_context():

        for provider in db.session.query(Provider).all():
            db.session.delete(provider)
        db.session.commit()

        ProvidersService().create(data)


        provider = db.session.query(Provider).where(Provider.name == 'Test Provider').first()

        assert provider is not None, 'Provider not found'
        assert provider.name == 'Test Provider'
        assert provider.address == 'Test Address'
        assert provider.active == True
        assert provider.phone == '1234567890'



def test_update_provider_service(client, db):
    login(client)
    
    

    with client.application.app_context():
        id = db.session.query(Provider).where(Provider.name == 'Test Provider').first().id

        data = {
            'provider_id': id,
            'name': 'Test Provider 2',
            'address' : 'Test Address 2',
            'active': False,
            'phone': '33',
            'email': 'test2@gmail.com'
        }

        ProvidersService().update(**data)

        provider = db.session.query(Provider).where(Provider.id == id).first()

        assert provider is not None
        assert provider.name != 'Test Provider'
        assert provider.address != 'Test Address'
        assert provider.active != True
        assert provider.phone != '1234567890'

def test_get_providers(client, db):
    login(client)
    
    data = {
        'name': 'Test Provider',
        'address' : 'Test Address',
        'active': True,
        'phone': '1234567890',
        'email': 'test@gmail.com'
    }

    with client.application.app_context():
        providers = ProvidersService().get_providers()
        assert len(providers) > 0