import flask.testing
import pytest
from store.app import create_app
import flask
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture
def app() -> flask.testing.FlaskClient:
    app = create_app('tests.database_config')
    return app

@pytest.fixture
def client(app : flask.Flask) -> flask.testing.FlaskClient:
    return app.test_client()

@pytest.fixture
def db(app) -> SQLAlchemy:
    from store.extensions import db as _db

    return _db