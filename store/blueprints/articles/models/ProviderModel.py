from store.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey, BOOLEAN, Text, Float
from sqlalchemy.orm import relationship, validates


class ProviderModel(db.Model):
    __tablename__ = 'provider'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(24), nullable=False)
    email = Column(String(256), nullable=False)
    address = Column(Text, nullable=False)
    
    active = Column(BOOLEAN, default=True)


    