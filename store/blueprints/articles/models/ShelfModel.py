from store.extensions import db

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from datetime import timedelta, datetime


class ShelfLifeModel(db.Model):
    __tablename__ = 'shelf_life'
    id = Column(Integer, primary_key=True)
    initial_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    article = relationship('ArticleModel', foreign_keys=[article_id])
    
    