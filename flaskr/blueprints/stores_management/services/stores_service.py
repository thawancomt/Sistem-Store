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
    
    def get_name_by_id(self, id):
        return Store.query.filter_by(id=id).first().name
    
    def create(self, store_name, store_id, store_place):
        store_id = int(store_id)
        
        store = Store(name=store_name, id=store_id, place=store_place)
        db.session.add(store)
        db.session.commit()