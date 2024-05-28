from flaskr.blueprints.users.models.UserModel import User # type: ignore
from flaskr.extensions import db
from datetime import datetime
from hashlib import sha256

from flaskr.blueprints.users.models.UserModel import User

from werkzeug.security import generate_password_hash, check_password_hash
def hash_password(password):
    return sha256(password.encode()).hexdigest()



class UserService:
    
    def __init__(self, **kwargs) -> None:
        self.db = db
        
    def create(self, name, email, password, store):
        
        password = generate_password_hash(password)
        
        new_user = User()
        new_user.username = name
        new_user.email = email
        new_user.password = password
        new_user.store = store
        new_user.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.db.session.add(new_user)
        self.db.session.commit()
    
    def delete_user_by_username(self, username) -> bool:
        if user := User.query.filter(User.username == username):
            user.delete()
            db.session.commit()
            return True

        return False
    
    def delete_user_by(self, id):
        user = User.query.filter_by(id=id).delete()
        db.session.commit()
    
    def update(self, username, data):
        if user := db.session.query(User).filter(User.username == username).first():
            user.username = data.get('new_username')
            user.email = data.get('email')
            user.store = data.get('store')
            
        db.session.commit()
        return user
    
    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).join()
        
    def get_user_by(self, id = None, username = None, email = None):
        if User.query.filter_by(id=id).first():
            return User.query.filter_by(id=id).first()
        
        if User.query.filter_by(username=username).first():
            return User.query.filter_by(username=username).first()
        
        if User.query.filter_by(email=email).first():
            return User.query.filter_by(email=email).first()
        
        return None
    
    def get_all(self):
        return User.query.all()
    


        