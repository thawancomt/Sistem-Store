from store.extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, func

from sqlalchemy.orm import relationship

class DailyTaskModel(db.Model):
    __tablename__ = 'daily_tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    
    description = Column(Text, nullable=False)
    
    status = Column(Boolean, server_default='1', nullable=False) 

    
    start_at = Column(DateTime,server_default=func.now() ,nullable=False)
    end_at = Column(DateTime, nullable=True)
    
    

    finished_by = Column(Integer, ForeignKey('users.id'))
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    

    finisher = relationship('User', foreign_keys=[finished_by] )
    creator = relationship('User', foreign_keys=[created_by] )
    
