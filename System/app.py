from flask import Flask, redirect, render_template, request, flash
from managers.users import User, Login, CreateUser, Session
from managers.production import Production, Consumes

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
        result = Session.connected_users[ip]['status']
        if result:
            return True
    except KeyError:
        return False


def login_required():
    return 'fodas'


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

        # Create a new user object and set email and password
        connected_user = User()
        connected_user.email = email
        connected_user.password = password

        # Validate return is Boolean
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
    return redirect('/login')


@app.route('/homepage/')
def redirect_home():
    # If the user enter on homepage without a date
    user_store = Session(request.remote_addr).store_name(id=True)
    return redirect(f'/homepage/{date.today()}/{user_store}')


@app.route('/homepage/<date_for>/<store_to_show>', methods=['GET', 'POST'])
def home(date_for, store_to_show):

    if is_user_logged_in(request.remote_addr):
        pass
    else:
        return redirect('/login')
    
    if request.method == 'POST':
        return redirect(f'/homepage/{date_for}/{request.form.get("store_by_select_form")}')

    user_store = Session(request.remote_addr).store_name(id=True)

    if user_data(date_for=date_for)['level'] == 'Administrador':

        # The store to show on page, if equal to store_to_show will show the url store Id
        user_store = store_to_show

        # Try to get the store by the select element in the homepage
        show_store_by_select_form = request.form.get('store_by_select_form')

        # if the store to show is from the select form
        if show_store_by_select_form:

            for store_id, store_name in Production.stores.items():
                if store_name == show_store_by_select_form:
                    show_store_by_select_form = store_id

            return render_template('homepage.html', data=user_data(date_for, store_to_show=int(show_store_by_select_form)),
                                   date_for=date_for,
                                   store_to_show=show_store_by_select_form,
                                   stores=Production.stores, users=User().return_filtered_users_by_store(int(store_to_show)))

        return render_template('homepage.html', data=user_data(date_for, store_to_show=user_store),
                               date_for=date_for,
                               store_to_show=store_to_show,
                               stores=Production.stores, users=User().return_filtered_users_by_store(int(store_to_show)))

    else:
        if int(user_store) != int(store_to_show):
            flash("You can't edit other store")
            return redirect('/homepage')

        data = user_data(date_for=date_for, store_to_show=user_store)

        return render_template('homepage.html', data=data, date_for=date_for, store_to_show=store_to_show,
                               stores=Production.stores, users=User().return_filtered_users_by_store(int(store_to_show)))


# @app.route('/show_store_production_if_admin')
# def show_store_production_if_admin():

#     if request.method == 'POST':
#         store = request.form.get('store_by_select_form')
#         store_to_send = 0
#         for store_id, store_name in Production.stores.items():
#             if store_name == store:
#                 store_to_send = store_id

#                 return render_template('homepage.html', )
#             else:
#                 return 'Store not found'
#     return r'teste'


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
    production.store = int(store_to_send)
    production.send_production()

    return redirect(f'/homepage/{date_for}/{store_to_send}')

@app.route('/consume/<date_for>/<store_to_send>', methods=['GET', 'POST'])
def enter_consume(date_for, store_to_send):
    consume = Consumes()
    consume.date = date_for
    consume.store = int(store_to_send)

    if request.method == 'POST':
        
        bread = request.form.get('bread')
        slice = request.form.get('slice')
        consume.worker = request.form.get('who_consume')

        consume.data = {'bread' : int(bread), 'slices' : int(slice)}
        consume.send_consume()

        return redirect('/homepage')


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def edit_logged_user():
    return render_template('user.html', username=Session(request.remote_addr).name())


@app.route('/edit/user/<username>', methods=['GET', 'POST'])
def edit_user(username):

    # set old user
    old_user = User()
    old_user.username = username

    # after set old user, get their data
    old_data = User().get_user_data(old_user)

    # with his data define the old user email
    old_user.email = old_data['email']

    if request.method == 'POST':

        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        new_email = request.form.get('new_email')
        new_store = int(request.form.get('new_store'))

        new_data = {
            'username' :  new_username,
            'password' : new_password,
            'email' : new_email,
            'store' : new_store
        }

        try:
        
            User().edit_user(old_user, new_data)
            return redirect(f'/edit/user/{new_data["username"]}')
        except KeyError:
            return 'ERROR EDITING USER'



    return render_template("edit_user.html", username=username, data=user_data(), old_data=old_data)


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

    if is_user_logged_in(request.remote_addr):
        pass
    else:
        return redirect('/login')

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
