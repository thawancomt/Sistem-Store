from flaskr.extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

class DailyStatusModel(db.Model):
    __tablename__ = 'daily_task_status'
    id = Column(Integer, primary_key=True)
    
    task_id = Column(Integer, ForeignKey('daily_tasks.id'))
    task = relationship('DailyTaskModel', foreign_keys=[task_id])
    
    status = Column(Boolean, server_default='0', nullable=False)
    date = Column(DateTime, nullable=False)