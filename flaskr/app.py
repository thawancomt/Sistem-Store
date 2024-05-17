from flask import Flask, redirect, render_template, request, flash
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flaskr.extensions import db, login_manager

from flaskr.blueprints.login.bp_login import login_bp
from flaskr.blueprints.home.views.bp_home import  home_bp
from flaskr.blueprints.users.views.bp_users import users_page_bp
from flaskr.blueprints.stock.bp_stock import stock_bp
from flaskr.blueprints.tasks.bp_tasks import tasks_bp



from datetime import datetime

def create_app():

    app = Flask(__name__)
    
    app.secret_key = b'2222'

    app.config.from_object('CONFIG')

    app.secret_key = '2222'
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(users_page_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(tasks_bp)
    
    db.init_app(app)
    login_manager.init_app(app)




    return app
