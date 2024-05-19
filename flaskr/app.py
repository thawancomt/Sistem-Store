from flask import Flask, redirect, render_template, request, flash, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flaskr.extensions import db, login_manager

from flaskr.blueprints.login.views.LoginView import login_bp
from flaskr.blueprints.homepage.views.Homepage import  homepage
from flaskr.blueprints.users.views.bp_users import users_page_bp
from flaskr.blueprints.tasks.views.TaskView import tasks_bp
from flaskr.blueprints.stores_management.view.StoreView import store_bp


from datetime import datetime

def create_app():

    app = Flask(__name__)
    
    app.secret_key = b'2222'

    app.config.from_object('CONFIG')

    app.secret_key = '2222'
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


    app.register_blueprint(login_bp)
    app.register_blueprint(homepage)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(store_bp)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)

    @app.route('/')
    def home():
        return redirect(url_for('home_bp.home'))



    return app
