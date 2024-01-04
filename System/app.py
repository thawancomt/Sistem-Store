from flask import Flask, redirect, render_template, request, flash
from managers.users import User, Login, CreateUser, Session
from managers.production import Production, Consumes, Wasted
from managers.analyses import Analyze
from managers.stores_management import Store


from datetime import date


app = Flask(__name__)

app.secret_key = '2222'


def user_data(date_for = '', store_to_show = 0):
    
    """
    This function is used to create a dictionary with all the data that is use
    to get the user data. This function is used to avoid the repetition of code
    
    :param date_for: The date to get the data
    :param store_to_show: The store to get the data

    :return: A dictionary with all the data

    """

    data = {}

    if not date_for:
        date_for = date.today()

    if store_to_show:
        data['total_of_the_day'] = Production(date_for).get_already_produced(store_to_show)
        data['store_name'] = Session(request.remote_addr).store_name()

    data['username'] = Session(request.remote_addr).name()
    data['level'] = Session(request.remote_addr).level()
    data['articles'] = Production.articles
    data['stores'] = Production.stores

    return data

def is_user_logged_in(ip):
    # Check if user is logged in
    try:
        result = Session.connected_users[ip]['status']
        if result:
            return True
    except KeyError:
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():

    # Check if the user is logged in, if true redirect to homepage
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

            # define this user as logged in
            Session.connected_users[request.remote_addr]['status'] = True

            # update the last login of user
            User().edit_user(who=connected_user,new_data={'last_login': str(date.today())})

            return redirect('/homepage/')
        else:
            flash('Incorrect email or password')

    return render_template('auth/login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Disconnect the user
    Session(request.remote_addr).disconnect_user()
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.route('/')
def index():
    return redirect('auth/login')

@app.route('/homepage/')
def redirect_home():
    # If the user enter on homepage without a date
    user_store = Session(request.remote_addr).store_name(id=True)
    return redirect(f'/homepage/{date.today()}/{user_store}')


@app.route('/homepage/<date_for>/<store_to_show>', methods=['GET', 'POST'])
def home(date_for, store_to_show):

    # Get the user store by Id (Id=False if want the name)
    user_store = Session(request.remote_addr).store_name(id=True)

    # Object to get management of the store
    store = Store()
    store.store = store_to_show


    # Check if the user is logged in, else redirect to login page
    if not is_user_logged_in(request.remote_addr):
        return redirect('/login')

    # Create a context to send to the template
    context = {}
    
    # User context
    context['store_to_show'] = store_to_show
    context['data'] = user_data(date_for, store_to_show)
    context['level'] = context['data']['level']

    # Store context
    context['workers'] = User().return_filtered_users_by_store(int(store_to_show))
    context['tasks'] = [store.get_all_tasks(date_for), store.get_concluded_tasks(date_for)]
    context['store_to_show'] = store_to_show
    context['date_for'] = date_for
    context['stores'] = Production.stores

    # Production context
    context['weekly_data'] = Production(date_for).create_data_to_ball_usage_chart(store_to_show, -30)
    context['dates'] = Production(date_for).create_data_to_ball_usage_chart(store_to_show, -7)['dates']

    # Consume context
    context['consumes'] = Consumes().get_consume_by_day(int(store_to_show), date_for)
    context['consume_data'] = Consumes().create_data_to_consume_chart(int(store_to_show), date_for)

    # Check if the user is allowed to edit and visualize the store
    if int(user_store) != int(store_to_show) and context['level'] != 'Administrador':
            flash("You can't edit other store")
            return redirect('/homepage/')
    
    # Handle the POST request
    if request.method == 'POST':

        store_to_redirect = request.form.get("store_by_select_form")

        context['store_to_show'] = int(store_to_redirect)

        return redirect(f'/homepage/{date_for}/{store_to_redirect}')


    return render_template('store/homepage.html', context=context, date_for=date_for, store_to_show=store_to_show)


@app.route('/production/<date_for>/<store_to_send>', methods=['GET', 'POST'])
def enter_production(date_for, store_to_send):

    if request.method == 'POST':

        # Get the old production data
        old_production = Production(date_for).get_already_produced(store_to_send)

        data_to_send_production = {}

        for article_id, article_name in Production.articles.items():
            data_to_send_production[article_id] = request.form.get(article_id, int(old_production[article_id]))

        # Create a new production objetct, set the value and send it
        production = Production(date_for, data_to_send_production)
        production.store = int(store_to_send)
        production.send_production()

    return redirect(f'/homepage/{date_for}/{store_to_send}')


@app.route('/consume/<date_for>/<store_to_send>', methods=['GET', 'POST'])
def enter_consume(date_for, store_to_send):

    if request.method == 'POST':

        # Get the data from the form
        data_to_send_consume = request.form.to_dict()

        # Create a consume objetct and set the date to send the consume and the store
        consume = Consumes()
        consume.worker = request.form.get('who_consume')

        # Set the data, date and store to send consumes
        consume.data = data_to_send_consume
        consume.date = date_for
        consume.store = int(store_to_send)

        consume.send_consume()

        return redirect(f'/homepage/{date_for}/{store_to_send}')


@app.route('/waste/<date_for>/<store_to_send>', methods=['GET', 'POST'])
def enter_waste(date_for, store_to_send):

    if request.method == 'POST':
        # Get the data from the form and delete the who consume
        data = request.form.to_dict()
        del data['who_consume']

        # create a new variable to receive who consume separately
        who = data['who_consume']

        
        for article, article_amount in data.items():
            
            if article_amount == '':
                data[article] = 0
            else:
                data[article] = int(article_amount)

        wasted = Wasted(date_for=date_for, store=int(store_to_send))

        wasted.worker = who
        wasted.data = data
        wasted.enter_wasted()

        return redirect('/homepage')


@app.route('/edit/user/<username>', methods=['GET', 'POST'])
def edit_user(username):

    if not is_user_logged_in(request.remote_addr):
        return redirect('/login')

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
            'username':  new_username,
            'password': new_password,
            'email': new_email,
            'store': new_store
        }

        User().edit_user(old_user, new_data)

        if username == user_data().get('username'):
            logout()

        if new_username:
            return redirect(f'/edit/user/{new_username}')
        else:
            return redirect(f'/edit/user/{old_data.get("username")}')

    context = {}
    context['data'] = user_data()
    context['old_data'] = old_data
    context['old_user'] = old_user
    context['username'] = username
    context['email'] = old_user.email

    return render_template("users/edit_user.html", context=context)

@app.route('/delete/user/', methods=['GET', 'POST'])
def delete_user():

    if request.method == 'POST':

        username = request.form.get('old_username')
        email = request.form.get('old_email')

        deleted_user = User()
        deleted_user.username = username
        deleted_user.email = email

        deleted_user.delete_user(email)

        if username == Session(request.remote_addr).name():
            logout()
            
        flash('User deleted')

    return redirect('/users')

@app.route('/register', methods=['GET', 'POST'])
def register_user():

    if request.method == 'POST':

        new_user = User()

        new_user.username = request.form.get('username')
        new_user.email = request.form.get('email')
        new_user.password = request.form.get('password')
        new_user.store = int(request.form.get('store'))
        new_user.level = request.form.get('level')
        new_user.last_login = ''
        new_user.when_was_created = str(date.today())

        CreateUser(new_user)

    context = {}
    context['data'] = user_data()
    context['levels'] = User.levels_of_users

    return render_template('auth/register.html', context=context)


@app.route('/users')
def show_users():

    if is_user_logged_in(request.remote_addr):
        pass
    else:
        return redirect('/login')

    context = {}

    context['data'] = user_data()
    context['users'] = User().return_all_users()

    return render_template('users/users.html', context=context)


@app.route('/users/search/', methods=['GET', 'POST'])
def show_users_filtered():
    """"
    The search function is designed to return the users whose usernames match
    the search query. If the search query is an empty string, then the search
    function returns all the users, because all the usernames are different 
    from. This is equivalent to showing the entire list of users without any
    filtering.'.
    """

    if is_user_logged_in(request.remote_addr):
        pass
    else:
        return redirect('/login')

    username = request.form.get('filter')
    filtered_users = User().return_filtered_users(username)

    context = {}
    context['data'] = user_data()
    context['users'] = filtered_users

    return render_template('users.html', data=user_data(), context=context)


@app.route('/tasks/<date_for>/<store_to_send>/<action>', methods=['GET', 'POST'])
def tasks(date_for, store_to_send, action):
    store = Store()
    store.store = store_to_send

    if request.method == 'POST':
        task_to_create = request.form.get('task_to_send')
        task_description = request.form.get('task_description')

        task_to_delete = request.form.to_dict()
        
        
        if action == 'create':
            store.create_task(date_for, task_to_create, task_description)

        elif action == 'delete':
            for task, value in task_to_delete.items():
                store.delete_task(date_for, task)
        elif action == 'concluded':

            for task, value in task_to_delete.items():
                store.task_concluded(date_for, task)

        return redirect(f'/homepage/{date_for}/{store_to_send}')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


