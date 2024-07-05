from store.blueprints import *


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
    
    if LoginService(email = email, password = password).login():
        return redirect(url_for('homepage.home'))
    
    flash('Invalid email or password', 'danger')
    return redirect(url_for('auth.login_page'))

@authentication.route('/logout')
def logout():
    LoginService().logout()
    return redirect(url_for('auth.login_page'))

    