import pytest
from store.app import create_app



@pytest.fixture
def app():
    app = create_app('tests.database_config')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    from store.extensions import db
    return db