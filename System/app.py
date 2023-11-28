from flask import Flask, redirect, render_template, request, flash
from managers.users import User, Login, CreateUser, Session
from managers.production import Production

from datetime import date


app = Flask(__name__)

app.secret_key = '2222'


def user_data(date_for="1999-01-01", store_to_show=5):

    if not date_for == "1999-01-01":
        data = {
            'username': Session(request.remote_addr).name(),
            'level': Session(request.remote_addr).level(),
            'articles': Production.articles,
            'store_name': Session(request.remote_addr).store_name(),
            'total_of_the_day': Production(date_for).get_already_produced(store_to_show),
            'stores': {
                3: 'Colombo',
                5: 'Odivelas',
                11: 'Campo de Ourique',
                25: 'Baixa Chiado'
            }
        }

        return data
    else:
        data = {
            'username': Session(request.remote_addr).name(),
            'level': Session(request.remote_addr).level(),
            'articles': Production.articles,
            'store_name': Session(request.remote_addr).store_name(),
            'stores': {
                3: 'Colombo',
                5: 'Odivelas',
                11: 'Campo de Ourique',
                25: 'Baixa Chiado'
            }
        }
        return data


def is_user_logged_in(ip):
    # Check if user is logged in
    try:
        if Session.connected_users[ip]['status']:
            return True
    except KeyError:
        return False


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if is_user_logged_in(request.remote_addr):
        return redirect('/homepage')

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

            # update the last login of user

            User().edit_user(who=connected_user,
                             new_data={'last_login': str(date.today())})

            # define this user as logged in
            Session.connected_users[request.remote_addr]['status'] = True

            return redirect('/homepage/')
        flash('Incorrect email or password')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    Session(request.remote_addr).disconnect_user()
    return redirect('/homepage/')


@app.route('/homepage/')
def redirect_home():
    user_store = Session(request.remote_addr).store_name(id=True)
    return redirect(f'/homepage/{date.today()}/{user_store}')


@app.route('/homepage/<date_for>/<store_to_show>')
def home(date_for, store_to_show):

    user_store = Session(request.remote_addr).store_name(id=True)

    if is_user_logged_in(request.remote_addr):
        pass
    else:
        return redirect('/login')

    if user_data(date_for=date_for)['level'] == 'Administrador':
        user_store = store_to_show
        return render_template('homepage.html', data=user_data(date_for, store_to_show=user_store), date_for=date_for, store_to_show=store_to_show)

    else:

        data = user_data(date_for=date_for, store_to_show=user_store)
        return render_template('homepage.html', data=data, date_for=date_for, store_to_show=store_to_show)


@app.route('/production/<date_for>/<store_to_send>', methods=['GET', 'POST'])
def enter_production(date_for, store_to_send):
    data = {}

    old_production = Production(date_for).get_already_produced(
        Session(request.remote_addr).store_name(id=True))

    if request.method == 'POST':

        for article_id, article_name in Production.articles.items():
            try:
                if request.form.get(article_id):

                    data[article_id] = int(request.form.get(article_id))

                else:
                    data[article_id] = int(old_production[article_id])

            except KeyError:
                data[article_id] = 0

    production = Production(date_for, data)
    production.store = Session(request.remote_addr).store_name(id=True)
    production.send_production()

    return redirect(f'/homepage/{date_for}/{store_to_send}')


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def edit_user():
    return render_template('user.html', username=Session(request.remote_addr).name())


@app.route('/register', methods=['GET', 'POST'])
def register_user():

    new_user = User()

    if request.method == 'POST':
        new_user.username = request.form.get('username')
        new_user.email = request.form.get('email')
        new_user.password = request.form.get('password')
        new_user.store = int(request.form.get('store'))
        new_user.level = request.form.get('level')
        new_user.last_login = ''
        new_user.when_was_created = str(date.today())

        CreateUser(new_user)

    return render_template('register.html', data={'stores': {
        3: 'Colombo',
        5: 'Odivelas',
        11: 'Campo de Ourique',
        25: 'Baixa Chiado'
    },
        'levels': ['Colaborador', 'Administrador', 'Visitante']})


@app.route('/users')
def show_users():
    return render_template('users.html', data=user_data(), users=User().return_all_users())


@app.route('/users/search/', methods=['GET', 'POST'])
def show_users_filtered():
    """"
    The search function is designed to return the users whose usernames match
    the search query. If the search query is an empty string, then the search
    function returns all the users, because all the usernames are different 
    from. This is equivalent to showing the entire list of users without any
    filtering.'.
    """
    username = request.form.get('filter')
    filtered_user = User().return_filtered_users(username)

    return render_template('users.html', data=user_data(), users=filtered_user)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
