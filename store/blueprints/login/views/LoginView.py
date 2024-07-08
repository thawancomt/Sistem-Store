from store.blueprints import *

from flask import jsonify


from ..services.LoginService import LoginService

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
        return redirect(url_for('auth.login_page'))
    
    if LoginService(email = email, password = password).login():
        return redirect(url_for('homepage.home'))
    
    flash('Invalid email or password', 'danger')
    return redirect(url_for('auth.login_page'))

@authentication.route('/logout')
def logout():
    LoginService().logout()
    return redirect(url_for('auth.login_page'))

@authentication.route('/view_code', methods=['GET'])
def register_page():
    from store.blueprints.users.services.UserService import UserService
    from store.micro_services.code_verification import CodeService
    
    email = request.form.get('email') or request.args.get('email')
    
    user = UserService(email=email).get_user_by_email()
    
    return jsonify({
        'check_code' : CodeService.check_code(user.id, request.args.get('code') or request.form.get('code')),
        'code' : request.args.get('email')
    })