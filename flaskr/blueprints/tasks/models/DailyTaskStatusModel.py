from flaskr.extensions import db

from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, DateTime

from sqlalchemy.orm import relationship


class DailyTaskStatusModel(db.Model):
    __tablename__ = 'daily_task_status'
    id = Column(Integer, primary_key=True, autoincrement=True)

    task_id = Column(Integer, ForeignKey('daily_tasks.id'), nullable=False)
    task = db.relationship('DailyTaskModel', foreign_keys=[task_id])


    status = Column(Boolean, nullable=False, server_default='0')
    date = Column(DateTime, nullable=False)
    fineshed_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', foreign_keys=[fineshed_by])