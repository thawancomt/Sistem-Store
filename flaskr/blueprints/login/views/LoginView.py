from flaskr.blueprints import *


from ..services.LoginService import LoginService

authentication = Blueprint('auth', __name__,
                     url_prefix='/auth')


@authentication.route('/', methods=['GET'])
def login_page():
    return render_template('auth/login.html')

@authentication.route('/', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if LoginService(email = email, password = password).login():
        return redirect(url_for('homepage.home'))
    
    return redirect(url_for('auth.login_page'))

@authentication.route('/logout')
def logout():
    LoginService().logout()
    return redirect(url_for('auth.login_page'))

    