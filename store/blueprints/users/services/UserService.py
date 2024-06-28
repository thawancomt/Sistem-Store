from store.blueprints.users.models.UserModel import User # type: ignore
from store.extensions import db
from datetime import datetime
from hashlib import sha256

from store.blueprints.users.models.UserModel import User

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
                 last_login : datetime = None
                ):
        
        self.db = db
        
        self.username = username
        self.email = email
        self.password = generate_password_hash(password) if password else None
        self.store_id = store_id
        self.created_at = datetime.now()
        self.last_login = datetime.now()
        
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
    @staticmethod
    def delete_user_by_id(id):
        if user := User.query.filter_by(id=id).one_or_none():
            UserService.update_user_status_to_inactive(id)
            return True
        return False
    
    @staticmethod
    def update_user_status_to_inactive(user_id: int) -> bool:
        if user := User.query.filter_by(id=user_id).one_or_none():
            user.active = False
            db.session.commit()
            return True
        return False
    
    def active_an_inactive_user(id) -> bool:
        if user := db.session.query(User).filter(
            User.id == id
        ).first():
            user.active = True
            db.session.commit()
            return True
        return False
    
    def update(self, username, data):
        if user := db.session.query(User).filter(User.username == username).first():
            user.username = data.get('new_username')
            user.email = data.get('email')
            user.store_id = data.get('store')
            user.level = data.get('level')
            user.password = generate_password_hash(data.get('password')) if data.get('password') else user.password
        
            db.session.commit()
        return user
    
    def get_all(self):
        return db.session.query(User).all()
    
    @staticmethod
    def get_all_active_users(query = None):
        if query:
            return db.session.query(User).filter(User.active == True,
                                                 User.username.like(f'%{query}%')).all()
        return db.session.query(User).filter(User.active == True).all()
    @staticmethod
    def get_all_inactive_users(query = None):
        if query:
            return db.session.query(User).where(User.active == False,
                                                 User.username.like(f'%{query}%')).all()
        return db.session.query(User).where(User.active == False).all()
    
    def get_user_by_email(self):
        return db.session.query(User).filter(User.email == self.email).first()
    
    def get_user_by_username(self):
        return db.session.query(User).filter(User.username ==  self.username).first()
    


        