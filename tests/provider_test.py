from tests.utils import *
from tests.login_test import login

def test_provider(client):
    login(client)

    data = {
        'name': 'Provider 1',
        'phone': '123456789',
        'email': 'teste@gmail.com',
        'address': 'Rua das flores'
    }

    client.post('/providers/create', data=data, content_type='application/x-www-form-urlencoded')

    


    

