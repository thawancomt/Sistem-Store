from flaskr.blueprints.users.models.UserModel import User # type: ignore
from flaskr.extensions import db
from datetime import datetime
from hashlib import sha256

from flaskr.blueprints.users.models.UserModel import User

from werkzeug.security import generate_password_hash, check_password_hash
def hash_password(password):
    return sha256(password.encode()).hexdigest()



class UserService:
    
    def __init__(self,
                 username : str= None, 
                 email : str = None,
                 password : str = None, 
                 store_id : str = None, 
                 created_at : datetime= None,
                 last_login : datetime = None) -> None:
        
        self.db = db
        
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) if password else None
        self.store_id = store_id
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def create(self):
        if new_user := self.db.session.query(User).filter(User.username == self.username).first():
            return False
        
        new_user = User(
            username = self.username,
            email=self.email,
            password = self.password,
            store_id = self.store_id,
            created_at = self.created_at,
            last_login = self.last_login
        )
        
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
            user.store_id = data.get('store')
            
        db.session.commit()
        return user
    
    def get_all(self):
        return User.query.all()
    
    def get_user_by_email(self):
        return db.session.query(User).filter(User.email == self.email).first()
    


        