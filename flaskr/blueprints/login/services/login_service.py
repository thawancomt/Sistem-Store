
from flaskr.blueprints.users.services.user_service import UserService, check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user

class LoginService:
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password
        self.user = UserService().get_user_by(email = self.email)
        
    def login(self):
        if self.user and self.verify_password(self.user.password):
            print(self.user.password)
            login_user(self.user)
            return True
        
        return False
    
    def verify_password(self, hashed_password):
        return check_password_hash(hashed_password, self.password)
        
    def login_user(self):
        login_user(self.user)
        
    def logout_user(self):
        logout_user()