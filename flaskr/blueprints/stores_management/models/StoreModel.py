from flaskr.extensions import db

class Store(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(50), nullable=False)