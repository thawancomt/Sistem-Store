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

    user = LoginService(email=email, password=True).user
    
    if user and not user.active:
        flash('User not active, check your email', 'danger')
        LoginService(email=email, password=True).send_code_to_active_account()
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
    
    user_id = request.args.get('id')
    user = UserService.get(int(user_id))
    
    if not user or user.active:
        return redirect(url_for('auth.login_page'))
    
    email = str(user.email)
    
    context = {
        'id' : user.id,
        'email' : email.replace(email[3:-3], '*' * len(email[2:-3]))
    }   
        
    return render_template('confirmation.html', context=context)

@authentication.route('/check_code', methods=['POST'])
def check_code():
    code_sent = request.form.get('code')
    user_id = request.form.get('user_id')

    if CodeService.check_code(user_id, code_sent):
        if request.args.get('pwd'):
            return redirect(url_for('auth.recovery_password', id=user_id, _method='POST'))
        
        if UserService.active_an_inactive_user(user_id):
            flash('Account activated', 'success')
            return redirect(url_for('auth.login_page'))
            
        flash('Account not activated', 'danger')
        return redirect(url_for('auth.login_page'))
    
    flash('Code is invalid', 'danger')
    return redirect(url_for('auth.confirmation',id=user_id))

@authentication.route('/recovery_password', methods=['GET', 'POST'])
def recovery_password():
    return render_template('recovery_password.html')

@authentication.route('/update_password', methods=['GET', 'POST'])
def check_code_password():
    email = request.form.get('email')
    user = UserService(email=email).get_user_by_email()
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('auth.recovery_password'))
    
    code = request.form.get('code')
    
    if CodeService.check_code(user.id, code):
        return redirect(url_for('auth.change_password', id=user.id))
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
    


@authentication.route('/change_password', methods=['GET', 'POST'])
def change_password():
    user_id = request.args.get('id')
    user = UserService.get(int(user_id))
    
    if request.method == 'POST':
        new_password = request.form.get('password')
        UserService().update(username=user.username, data={'password' : new_password})
        flash('Password changed', 'success')
    
        return redirect(url_for('auth.login_page'))

    
    return render_template('change_password.html', user=user)



