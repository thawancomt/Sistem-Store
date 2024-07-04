from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


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