
from flaskr.blueprints.users.services.UserService import UserService, check_password_hash
from flaskr.blueprints.users.models.UserModel import User, db

from flask_login import login_user, logout_user
from flaskr.extensions import login_manager

from flask import  redirect, flash, url_for

from datetime import datetime

class LoginService:
    def __init__(self, email = None, password = None) -> None:
        
        if email is None or password is None:
            return self.logout()
        
        self.email = email
        self.password = password
        self.user = UserService(email=self.email).get_user_by_email()
        
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(
            User
        ).filter(
            User.id == user_id
        ).first()
        
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash("You don't have appropriate access to view this page")
        return redirect(url_for('auth.login'))
    
    
    
    def login(self):
        if self.user and self.verify_password(self.user.password):
            self.user.last_login = datetime.now()
            db.session.commit()            
            login_user(self.user)
            return True
        
        return False
    
    def verify_password(self, hashed_password):
        return check_password_hash(hashed_password, self.password)

    def logout(self):
        logout_user()
    def exits1(self, email):
        return User.query.filter(User.email == email).first()