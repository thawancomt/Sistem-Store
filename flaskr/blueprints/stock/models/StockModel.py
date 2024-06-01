
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, func, and_
from sqlalchemy.orm import relationship


from flaskr.extensions import db

class Stock(db.Model):
    __tablename__ = 'stock'


    id = Column(Integer, primary_key=True)
    
    date = Column(DATETIME, default=db.func.now(), nullable=False)
    
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    store = relationship('Store', foreign_keys=[store_id])
    
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    article = relationship('ArticleModel',foreign_keys=[article_id])
    
    quantity = Column(Integer, nullable=False)
    
    def __repr__(self) -> str:
        return db.session.query(Stock).all()