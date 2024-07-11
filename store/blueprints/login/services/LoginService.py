
from store.blueprints.users.services.UserService import UserService, check_password_hash
from store.blueprints.users.models.UserModel import User, db
from store.micro_services.code_verification import CodeService
from store.micro_services.email_sender import Email

from flask_login import login_user, logout_user
from store.extensions import login_manager

from flask import  redirect, flash, url_for

from datetime import datetime, timedelta

class LoginService:
    def __init__(self, email = None, password = None) -> None:
        
        if email is None or password is None:
            return self.logout()
        
        self.email = email
        self.password = password
        self.user = UserService(email=self.email).get_user_by_email()
        
    @login_manager.user_loader
    def load_user(user_id):
        return UserService.get(user_id)
        
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash("You don't have appropriate access to view this page")
        return redirect(url_for('auth.login'))
    
    
    
    def login(self):
        if self.user and self.verify_password(self.user.password) and self.user.active:
            self.user.last_login = datetime.now() 
            db.session.commit()            
            login_user(self.user, remember=True, duration=timedelta(minutes=30))
            return True
        return False
    
    def verify_password(self, hashed_password):
        return check_password_hash(hashed_password, self.password)

    def logout(self):
        logout_user()
        
    def send_code_to_active_account(self):
        Email(self.user.email, id=self.user.id).send_email(code=True)
        
        