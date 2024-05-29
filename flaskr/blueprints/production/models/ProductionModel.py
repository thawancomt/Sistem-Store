from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from flaskr.extensions import db


class Production(db.Model):
    __tablename__ = 'production'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    store = relationship('Store', foreign_keys=[store_id] )
    article = relationship('ArticleModel', foreign_keys=[article_id] )
    creator = relationship('User', foreign_keys=[creator_id]) 