from flask import Flask, redirect, render_template, request, flash
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_sqlalchemy import SQLAlchemy

from flaskr.extensions import db

from flaskr.models import *

from flaskr.blueprints.login.bp_login import login_bp
from flaskr.blueprints.home.bp_home import  home_bp
from flaskr.blueprints.users.bp_users import users_page_bp
from flaskr.blueprints.stock.bp_stock import stock_bp
from flaskr.blueprints.tasks.bp_tasks import tasks_bp



from datetime import date

def create_app():

    app = Flask(__name__)

    app.config.from_object('CONFIG')

    app.secret_key = '2222'
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(users_page_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(tasks_bp)
    
    db.init_app(app)

    def external_ip():
        return request.remote_addr



    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.route('/')
    def index():
        return redirect('/login')



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


    return app
