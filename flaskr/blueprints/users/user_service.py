from flaskr.blueprints.users.users_model import User # type: ignore
from flaskr.extensions import db

from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()



class UserService:
    
    def __init__(self) -> None:
        self.db = db
        self.db.create_all()
        
    def create(self, name, email, password):
        
        password = hash_password(password)
        
        new_user = User()
        new_user.username = name
        new_user.email = email
        new_user.password = password
        
        self.db.session.add(new_user)
        self.db.session.commit()