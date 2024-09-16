from store.extensions import *
from store.utils import *

from ..services.LoginService import LoginService
from ...users.services.UserService import UserService

from store.micro_services.code_verification import CodeService

class LoginView(BlueprintBase):
    def __init__(self, name=None, static_folder=None, url_prefix=None, template_folder=None, import_name=None,) -> None:
        super().__init__(name, static_folder, url_prefix, template_folder, import_name)
        self.register_routes()

    def register_routes(self):
        self.blueprint.add_url_rule('/', 'auth', self.index, methods=['GET'])
        self.blueprint.add_url_rule('/login', 'login', self.login, methods=['GET','POST'])
        self.blueprint.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])
        self.blueprint.add_url_rule('/confirmation', 'confirmation', self.confirm_login, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/check_code', 'check_code', self.check_code, methods=['POST'])
        self.blueprint.add_url_rule('/recovery_password', 'recovery_password', self.recovery_password, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/update_password', 'update_password', self.update_password, methods=['GET', 'POST'])
        self.blueprint.add_url_rule('/check_code_password', 'check_code_password', self.check_code_password, methods=['POST'])
    
    def index(self):
        if current_user.is_authenticated and login_fresh():
            return redirect(url_for('homepage.index'))
        return render_template('login.html')
    
    def login(self):
        email, password = request.form.get('email'), request.form.get('password')

        user = LoginService(email=email, password=True)
        user = user.user
        
        if user and not user.active:
            flash('User not active, check your email', 'danger')
            LoginService(email=email, password=True).send_code_to_active_account()
            return redirect(url_for('auth.confirmation', id=user.id))
        
        if LoginService(email = email, password = password).login():
            return redirect(url_for('homepage.index'))
        
        flash('Invalid email or password', 'danger')
        return redirect(url_for('auth.auth'))


    def logout(self):
        LoginService().logout()
        return redirect(url_for('auth.auth'))
    
    def confirm_login(self):
        user_id = request.args.get('id')
        user = UserService.get(int(user_id))

        if not user or user.active:
            return redirect(url_for('auth.auth'))
        
        email = str(user.email)

        context = {
            'id' : user.id,
            'email' : email.replace(email[3:-3], '*' * len(email[2:-3]))
        }

        return render_template('confirmation.html', **context)

    def check_code(self):
        code_sent , user_id= request.form.get('code'), request.form.get('user_id')

        if CodeService.check_code(user_id, code_sent):
            if request.args.get('pwd'):
                return redirect(url_for('auth.recovery_password', id=user_id, _method='POST'))
            
            if UserService.active_an_inactive_user(user_id):
                flash('Account activated', 'success')
                return redirect(url_for('auth.auth'))
                
            flash('Account not activated', 'danger')
            return redirect(url_for('auth.auth'))
        
        flash('Code is invalid', 'danger')
        return redirect(url_for('auth.confirmation',id=user_id))
    
    def recovery_password(self):
        return render_template('recovery_password.html')
    

    def update_password(self):
        user_id = request.args.get('id')
        user = UserService.get(int(user_id))
        
        if request.method == 'POST':
            new_password = request.form.get('password')
            UserService().update(username=user.username, data={'password' : new_password})
            flash('Password changed', 'success')
        
            return redirect(url_for('auth.auth'))
    
        return render_template('change_password.html', user=user)
    
    def check_code_password(self):
        email = request.form.get('email')
        user = UserService(email=email).get_user_by_email()
        
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('auth.recovery_password'))
        
        code = request.form.get('code')
        
        if CodeService.check_code(user.id, code):
            return redirect(url_for('auth.update_password', id=user.id))
        else:
            if code:
                flash('code is invalid', 'danger')
        
        LoginService(email=email, password=True).send_code_to_active_account()
        context = {
        'id' : user.id,
        'email' : email.replace(email[3:-3], '*' * len(email[2:-3])),
        'normal_email' : email
        }
        return render_template('confirmation_password.html', context=context)
    
    def update(self):

        return super().update()
    def create(self):

        return super().create()
    def delete(self):

        return super().delete()

LoginView = LoginView('auth', static_folder= '..../static', url_prefix='/auth', template_folder='../templates', import_name=__name__).blueprint
