from flask import Blueprint, request, redirect, render_template, flash, url_for

from flaskr.models.users import Session, Login, User

from datetime import datetime

login_bp = Blueprint('login_bp', __name__,
                     url_prefix='/login')

def external_ip():
    return request.remote_addr

def is_user_logged_in(ip):
    # Check if user is logged in
    try:
        result = Session.connected_users[ip]['status']
        if result:
            return True
    except KeyError:
        return False

@login_bp.route('/', methods=['GET'])
def login_page():
    
    
    # Check if the user is logged in, if true redirect to homepage
    if is_user_logged_in(external_ip()):
        return redirect('/homepage')
    
    return render_template('auth/login.html')

@login_bp.route('/log_in', methods=['POST'])
def log_in():
    date = datetime.now().strftime('%Y-%m-%d')

    data : dict = request.form.to_dict()
    
    user_email = data.get('email', '')
    user_password = data.get('password', '')
    
    connected_user = User()
    connected_user.email = user_email
    connected_user.password = user_password
    
    result = Login(connected_user).validate()
    
    Session(external_ip(), connected_user).connect_user()
    
    
    
        
    return redirect(url_for('home_bp.home'))
    