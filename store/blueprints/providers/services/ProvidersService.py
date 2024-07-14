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
    def get(provider_id):
        return db.session.query(Provider).where(Provider.id == provider_id).first()
    
    @staticmethod
    def create(data):
        new_provider = Provider(**data)
        db.session.add(new_provider)
        db.session.commit()
        return new_provider
    @staticmethod
    def update(**data):
        provider_id = data.get('provider_id')
        
        provider = ProvidersService.get(provider_id)
        del data['provider_id']
        
        provider = ProvidersService.get(provider_id)
        for key, value in data.items():
            setattr(provider, key, value)
        
        
        db.session.commit()
        
    def delete(self, data):
        pass