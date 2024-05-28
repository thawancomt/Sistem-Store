from flask_sqlalchemy import SQLAlchemy

from flaskr.extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Task(db.Model):

    __tablename__ = 'store_tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(600), nullable=False)
    status = Column(String(100), nullable=False)

    # Relationship with users table (foreign keys already define the reference)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    finished_by = Column(Integer, ForeignKey('users.id'))

    # Relationship with users table (using relationship for clarity)
    created = relationship('User', foreign_keys=[created_by])
    finisher = relationship('User', foreign_keys=[finished_by])
