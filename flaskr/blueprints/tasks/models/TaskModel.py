from flask_sqlalchemy import SQLAlchemy

from flaskr.extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, Text, func, DateTime, Boolean
from sqlalchemy.orm import relationship



class Task(db.Model):
    __tablename__ = 'users_tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Boolean, server_default='0', nullable=False)

    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    finished_by = Column(Integer,ForeignKey('users.id'), server_default=None )
    
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    finished_at = Column(DateTime, nullable=True)



    creator = relationship('User', foreign_keys=[created_by])
    finisher = relationship('User', foreign_keys=[finished_by])
    