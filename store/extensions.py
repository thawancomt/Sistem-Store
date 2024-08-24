from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, fresh_login_required, LoginManager, current_user


from abc import ABC, abstractmethod

login_manager = LoginManager()

db = SQLAlchemy()

class Service(ABC):
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass


class BlueprintBase(ABC):
    @abstractmethod
    def register_routes(self):
        pass
    
    @abstractmethod
    def index(self):
        pass
    
    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass
    