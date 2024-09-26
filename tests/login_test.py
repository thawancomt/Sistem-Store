from tests.utils import *

def login(client):
    # Função auxiliar para fazer o login
    return client.post(
        '/auth/login',
        data={'email': 'admin@gmail.com', 'password': 'admin'},
        content_type='application/x-www-form-urlencoded'
    )

def test_login(client):
    # Usando o mesmo client para login e outras requisições
    response = login(client)

    assert response.status_code == 302, 'Login falhou'

    ind = client.get('/index')
    assert ind.location == 'http://localhost/index/', 'Login não redirecionou para /index/'

def test_logout(client):
    # Realizando login antes de testar logout
    login(client)

    # Fazendo logout
    response = client.get('/auth/logout')
    assert response.location == '/auth/', 'Logout não redirecionou para /auth/'