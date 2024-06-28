from store.extensions import db

from sqlalchemy.orm import validates

class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    
    @validates('name')
    def validate_name(self, key, value):
        if not 1 <= len(value) <= 50:
            raise ValueError('The store need a name')
        return value
    
    @validates('place')
    def validate_place(self, key, value):
        if not 1 <= len(value) <= 50:
            raise ValueError('Select the store location')
        return value
