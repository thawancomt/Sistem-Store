from ..models.store_model import Store
from flaskr.extensions import db

class StoresService:
    def create(self):
        pass
    def delete(self):
        pass
    def update(self):
        pass
    def get_by_id(self, id):
        return Store.query.filter_by(id=id).first()
    
    def get_all(self):
        return Store.query.all()
