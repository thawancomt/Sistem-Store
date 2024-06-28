
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, and_
from sqlalchemy.orm import relationship


from store.extensions import db

class Stock(db.Model):
    __tablename__ = 'stock'


    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, default=db.func.now(), nullable=False)
    
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    store = relationship('Store', foreign_keys=[store_id])
    
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    article = relationship('ArticleModel',foreign_keys=[article_id])
    
    quantity = Column(Integer, nullable=False)
