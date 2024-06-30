from store.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, Text
from sqlalchemy.orm import relationship, validates


class ArticleModel(db.Model):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    is_producible = Column(BOOLEAN, default=True, nullable=False)
    type_unit = Column(Integer, ForeignKey('type_units.id', ondelete='CASCADE'), nullable=False)
    stockable = Column(BOOLEAN, default=True, nullable=False)
    type = relationship('TypeUnitModel', foreign_keys=[type_unit])
    
    active = Column(BOOLEAN, default=True, nullable=False)
    
    
    
    
    @validates('name')
    def validate_name(self, key, value):
        if not value.strip():
            raise ValueError("The article must have a name")
        return value
    
class TypeUnitModel(db.Model):
    __tablename__ = 'type_units'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    alias = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)