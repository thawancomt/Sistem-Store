from flask_sqlalchemy import SQLAlchemy

from flaskr.extensions import db

class Task(db.Model):
    
    __tablename__ = 'store_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(600), nullable=False)