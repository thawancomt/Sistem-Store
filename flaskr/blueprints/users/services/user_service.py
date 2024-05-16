from flaskr.blueprints.users.models.users_model import User # type: ignore
from flaskr.extensions import db
from datetime import datetime
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()



class UserService:
    
    def __init__(self) -> None:
        self.db = db
        self.db.create_all()
        
    def create(self, name, email, password, store):
        
        password = hash_password(password)
        
        new_user = User()
        new_user.username = name
        new_user.email = email
        new_user.password = password
        new_user.store = store
        new_user.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.db.session.add(new_user)
        self.db.session.commit()
    
    def delete(self, id):
        user = User.query.filter_by(id=id).delete()
        db.session.commit()
    
    def update(self, id, name, email, password,store):
        
        user = User.query.filter_by(id=id)
        
        user.update(
            {
                "username": name or user.username,
                "email": email or user.email,
                "password": hash_password(password) or user.password,
                'last_login': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'store' : store or user.store
            }
        )
        
    def get_user_by(self, id = None, username = None, email = None):
        if User.query.filter_by(id=id).first():
            return User.query.filter_by(id=id).first()
        
        if User.query.filter_by(username=username).first():
            return User.query.filter_by(username=username).first()
        
        if User.query.filter_by(email=email).first():
            return User.query.filter_by(email=email).first()
        
        return None


        