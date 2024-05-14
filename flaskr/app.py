from flask import Flask, redirect, render_template, request, flash
from werkzeug.middleware.proxy_fix import ProxyFix

from flaskr.models import *

from flaskr.blueprints.login.bp_login import login_bp
from flaskr.blueprints.home.bp_home import  home_bp
from flaskr.blueprints.users.bp_users import users_page_bp

from datetime import date


app = Flask(__name__)

app.secret_key = '2222'
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(users_page_bp)


def external_ip():
    return request.remote_addr



@app.route('/logout', methods=['GET', 'POST'])
def logout():

    if is_user_logged_in(external_ip()):

        # Set the user that gonna be disconnected
        user = User()
        user.username = user_data().get('username')
        user.email = user_data().get('email')

        # Disconnect the user
        Session(external_ip(), user).disconnect_user()

    return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.route('/')
def index():
    return redirect('/login')

    # If the user enter on homepage without a date



@app.route('/production/<date_for>/<store_to_send>', methods=['GET', 'POST'])
def enter_production(date_for, store_to_send):

    if request.method == 'POST':
        # return request.form.to_dict()
        # Get the old production data
        old_production = Production(date_for).get_already_produced(store_to_send)

        data_to_send_production = {}

        for article_id, article_name in Production.articles.items():
            data_to_send_production[article_id] = int(request.form.get(article_id, 0))

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

        # Create a consume object and set the date to send the consume and the store
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
        # Get the data from the form and delete who consume
        data = request.form.to_dict()

        # create a new variable to receive who consume separately
        who = data['who_consume']

        # delete who consume from the data
        if data.get('who_consume'):
            del data['who_consume']

        # Before the treat of inputed data was here, but I change the treat handler to the DB manager
        # If some value is not int, the db return False and don't insert consume

        for article, article_amount in data.items():
            if article_amount == '':
                data[article] = 0
            else:
                data[article] = article_amount

        wasted = Wasted(date_for=date_for, store=int(store_to_send))

        wasted.worker = who
        wasted.data = data
        wasted.enter_wasted()

        return redirect('/homepage')


@app.route('/edit/user/<username>', methods=['GET', 'POST'])
def edit_user(username):

    if not is_user_logged_in(external_ip()):
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

        deleted_user.delete_user(deleted_user)

        if username == Session(external_ip()).name():
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

        if CreateUser(new_user).create_user():
            flash(True)
            return redirect('/login')
        else:
            flash(False)


    context = {}
    context['stores'] = Production.stores
    context['levels'] = User.levels_of_users

    return render_template('auth/register.html', context=context)



@app.route('/users/search/', methods=['GET', 'POST'])
def show_users_filtered():
    """"
    The search function is designed to return the users whose usernames match
    the search query. If the search query is an empty string, then the search
    function returns all the users, because all the usernames are different
    from. This is equivalent to showing the entire list of users without any
    filtering.'.
    """

    if is_user_logged_in(external_ip()):
        pass
    else:
        return redirect('/login')

    username = request.form.get('filter')
    filtered_users = User().return_filtered_users(username)

    context = {}
    context['data'] = user_data()
    context['users'] = filtered_users

    return render_template('users/users.html', data=user_data(), context=context)


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


@app.route('/stock/<store_to_show>/<reference>/<date>', methods=['GET', 'POST'])
def stock(store_to_show, date = 'last', reference = 'reference', chart_lenght = 0):

    if not is_user_logged_in(external_ip()):
        return redirect('/login')

    context = {}

    context['data'] = user_data(1, 5)
    context['articles'] = StockArticles().get_all_articles()
    context['store_stock'] = StoreStock().get_store_stock(store_to_show, date=date)
    context['reference_count'] = StoreStock().get_store_stock(store_to_show, date=reference)
    context['count_dates'] = StoreStock().get_stocks_dates(store_to_show)
    context['difference'] = StoreStock().get_difference(store_to_show, reference=reference)
    context['data_to_chart'] = StoreStock().create_data_to_chart(store_to_show, 4)

    if request.method == 'POST':
        stock_count = request.form.to_dict()

        if 'create_articles' in request.form.to_dict():
            articles_obj = StockArticles()

            article = request.form.get('create_articles')

            # Check if the input is multiple or single article
            if article:
                if ',' in article:
                    article_list = article.split(',')
                    articles_obj.insert_multiples_articles(article_list)
                else:
                    articles_obj.insert_new_article(article)



        # If reference_count is in the request dict, redirect user to page to view this reference
        # stock aside the last stock count
        elif 'reference_count' in request.form.to_dict().keys():
            reference = request.form.get('reference_count')
            return redirect(f'/stock/{store_to_show}/{reference}/last')

        elif 'date' in stock_count.keys():
            context['store_stock'] = StoreStock().get_store_stock(store_to_show, date=date)
            return redirect(stock_count.get('date'))
        else:
            StoreStock().enter_stock(int(store_to_show), 0, stock_count)

        return redirect(f'/stock/{store_to_show}/{reference}/last')

    return render_template('/store/stock_page.html', context=context)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
