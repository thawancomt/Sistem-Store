from store.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, Text, Float
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
    
    shelf_life = Column(Integer, default=1, nullable=False)
    
    active = Column(BOOLEAN, default=True, nullable=False)
    
    
    price = (Column(Float,server_default="0.0", nullable=False))
    is_in_promotion = Column(BOOLEAN, default=False, nullable=False)
    
    
    
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