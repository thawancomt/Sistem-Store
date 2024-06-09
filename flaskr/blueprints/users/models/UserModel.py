from flaskr.extensions import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, validates



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    last_login = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    level = Column(Integer, server_default='2', nullable=False)
    
    @validates('username')
    def validate_username(self, key, value):
        if not value.strip():
            raise ValueError('The username can not be empty')
        return value
    
    
    active = Column(Boolean, server_default='1', nullable=False)
    
    store_name = relationship("Store", foreign_keys=[store_id])
    

"""
    levels:
    0 - Admin
    1 - Manager
    2 - Employee

"""