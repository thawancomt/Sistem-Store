from flaskr.extensions import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    store = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)