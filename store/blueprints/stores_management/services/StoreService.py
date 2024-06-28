from ..models.StoreModel import Store
from store.extensions import db

class StoreService:
    def __init__(self, store_name = None, store_id = None, store_place = None) -> None:
        self.store_name = store_name
        self.store_id = int(store_id) if store_id else None
        self.store_place = store_place
        
    def create(self):
        new_store = Store()
        new_store.name = self.store_name
        new_store.id = self.store_id
        new_store.place = self.store_place
        
        
        db.session.add(new_store)
        db.session.commit()
        
    def get_by_id(self, id):
        return Store.query.filter_by(id=id).first()
    
    def get_all_stores(self):
        return Store.query.all()
    
    def get_name_by_id(self, id):
        return Store.query.filter_by(id=id).first().name
    