from flaskr.extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship




class DailyTaskModel(db.Model):
    __tablename__ = 'daily_tasks'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    store = relationship('Store', foreign_keys=[store_id])
    
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    active = Column(Boolean, server_default='1', nullable=False)
    
    status = Column(Boolean, server_default='0', nullable=False)
    
    creator = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', foreign_keys=[creator])
    
    start_date = Column(DateTime, nullable=False, server_default=func.now())
    end_date = Column(DateTime, nullable=True)