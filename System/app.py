from flask import Flask, redirect, render_template, request, flash
from managers.users import User, Login, CreateUser, Session
from production import Production

from datetime import date


app = Flask(__name__)


def is_user_logged_in(ip):
    # Check if user is logged in
    try:
        if Session.connected_users[ip]['status']:
            return True
    except:
        return False


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        connected_user = User()
        connected_user.email = email
        connected_user.password = password

        result = Login(connected_user).validate()

        if result:
            # insert the user into the logged users
            Session(request.remote_addr, connected_user).connect_user()

            # define this user as logged in
            Session.connected_users[request.remote_addr]['status'] = True

            return redirect('/homepage/')

    return render_template('login.html')


@app.route('/loggout')
def loggout():
    Session(request.remote_addr).disconnect_user()
    return redirect('/homepage/')


@app.route('/homepage/')
def redirect_home():
    return redirect(f'/homepage/{date.today()}')


@app.route('/homepage/<date_for>')
def home(date_for):

    if is_user_logged_in(request.remote_addr):
        pass
    else:
        return redirect('/login')

    return render_template('homepage.html', data={
        'username': Session(request.remote_addr).name(),
        'level': Session(request.remote_addr).level(),
        'articles': Production.articles,
        'store_name': Session(request.remote_addr).store_name()
    }, date_for=date_for)


@app.route('/production/<date_for>', methods=['GET', 'POST'])
def enter_production(date_for):
    data = {}
    if request.method == 'POST':
        for article_id, article_name in Production.articles.items():

            if request.form.get(article_id) == '':
                data[article_id] = 0
            else:
                data[article_id] = int(request.form.get(article_id))

    production = Production(data, date_for)
    production.store = Session(request.remote_addr).store_name(id=True)
    production.send_production()

    return redirect('/homepage/')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
