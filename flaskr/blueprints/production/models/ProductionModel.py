import flask_sqlalchemy.model
from flaskr.extensions import db

from sqlalchemy import Column, Integer, String, DATETIME

class Production(db.Model):
    __tablename__ = 'production'
    store = Column('store', Integer, primary_key=True, autoincrement=False, nullable=False)
    date = Column('date', DATETIME, primary_key=True, autoincrement=False, nullable=False)
    release_at = Column('release_at', DATETIME, autoincrement=False, nullable=False)
    item = Column('item', String(50), autoincrement=False, nullable=False)
    amount = Column('amount', Integer, nullable=False)
