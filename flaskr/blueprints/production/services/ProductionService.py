from flaskr.extensions import db
from ..models.ProductionModel import Production

class ProductionService:
    def get_all():
        return db.session.query(Production).all()