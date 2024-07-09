from store.blueprints import *

from flask import jsonify


from ..services.LoginService import LoginService

from store.blueprints.users.services.UserService import UserService

from store.micro_services.code_verification import CodeService

from flask_login import current_user, login_fresh

authentication = Blueprint('auth', __name__,
                     url_prefix='/auth',
                     template_folder='../templates',
                     static_folder='..../static')


@authentication.route('/', methods=['GET'])
def login_page():
    if current_user.is_authenticated and login_fresh():
        return redirect(url_for('homepage.home'))
    return render_template('login.html')

@authentication.route('/', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not (user := LoginService(email = email, password=True).user.active):
        flash('User not active, check your email', 'danger')
        LoginService(email = email, password = password).send_code_to_active_account()
        
        user = LoginService(email = email, password=True).user
        
        return redirect(url_for('auth.confirmation', id=user.id))
    
    if LoginService(email = email, password = password).login():
        return redirect(url_for('homepage.home'))
    
    flash('Invalid email or password', 'danger')
    return redirect(url_for('auth.login_page'))

@authentication.route('/logout')
def logout():
    LoginService().logout()
    return redirect(url_for('auth.login_page'))

@authentication.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    
    user = UserService.get(int(request.args.get('id')))
    
    if user.active:
        return redirect(url_for('auth.login_page'))
    
    email = str(user.email)
    
    context = {
        'id' : user.id,
        'email' : email.replace(email[2:-3], '*' * len(email[2:-3]))
    }
    
    if request.method == 'POST':
        
        code_sent = request.form.get('code')
        
        
        if CodeService.check_code(user.id, code_sent):
            user.active = True
            UserService.active_an_inactive_user(user.id)
            flash('Account activated', 'success')
            return redirect(url_for('auth.login_page'))
        
        flash('Code is invalid', 'danger')
        return redirect(url_for('auth.confirmation', id=user.id))
        
        
    return render_template('confirmation.html', context=context)