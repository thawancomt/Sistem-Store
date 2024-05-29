from flaskr.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ArticleModel(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(100), nullable=False)
    type_unit = Column(Integer, ForeignKey('type_units.id', ondelete='CASCADE'), nullable=False)
    
    type = relationship('TypeUnitModel', foreign_keys=[type_unit])
    
class TypeUnitModel(db.Model):
    __tablename__ = 'type_units'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    alias = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)