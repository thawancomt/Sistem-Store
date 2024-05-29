from flask import Flask, redirect, render_template, request, flash, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


from flaskr.extensions import db, login_manager

from flaskr.blueprints.login.views.LoginView import authentication
from flaskr.blueprints.homepage.views.Homepage import  homepage
from flaskr.blueprints.users.views.UsersPageView import users_page
from flaskr.blueprints.tasks.views.TaskView import tasks
from flaskr.blueprints.stores_management.view.StoreView import store
from flaskr.blueprints.articles.views.ArticlesView import articles
from flaskr.blueprints.production.views.ProductionView import production

from datetime import datetime

def create_app():

    app = Flask(__name__)
    
    app.secret_key = b'2222'

    app.config.from_object('CONFIG')


    app.register_blueprint(authentication)
    app.register_blueprint(homepage)
    app.register_blueprint(tasks)
    app.register_blueprint(store)
    app.register_blueprint(users_page)
    app.register_blueprint(articles)
    app.register_blueprint(production)


    migrate = Migrate(app, db)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)

    @app.route('/')
    def home():
        return redirect(url_for('homepage.home'))
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('/error/404.html'), 404


    return app
