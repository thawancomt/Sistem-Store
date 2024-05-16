
from flaskr.blueprints.users.services.user_service import UserService, hash_password

class LoginService:        
    def login(self, email, password):
        user = UserService().get_user_by(email = email)

        return user.username