from store.extensions import db

from store.blueprints.articles.models.ProviderModel import ProviderModel as Provider

class ProvidersService():
    def __init__(self) -> None:
        pass
    @staticmethod
    def get_providers():
        return db.session.query(Provider).all()
    @staticmethod
    def get_active_providers():
        return db.session.query(Provider).where(Provider.active == True).all()
    
    @staticmethod
    def create(data):
        new_provider = Provider(**data)
        db.session.add(new_provider)
        db.session.commit()
        return new_provider
    
    def update(self, data):
        pass
    def delete(self, data):
        pass