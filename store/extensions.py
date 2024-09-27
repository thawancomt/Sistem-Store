from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, fresh_login_required, LoginManager, current_user, login_fresh

from flask import Blueprint, flash


from abc import ABC, abstractmethod

login_manager = LoginManager()

db : SQLAlchemy = SQLAlchemy()

class Service(ABC):
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass


class BlueprintBase(ABC):
    def __init__(self, name = None, static_folder = None, url_prefix = None, template_folder = None, import_name = None) -> None:
        self.blueprint = Blueprint(
            name=name,
            import_name=import_name, 
            template_folder=template_folder,
            static_folder=static_folder,
            url_prefix=url_prefix,
        )
        
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
    