from flaskr.extensions import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship, declarative_base

base = declarative_base()



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    last_login = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    active = Column(BOOLEAN, nullable=False)
    
    store_name = relationship("Store", foreign_keys=[store_id])