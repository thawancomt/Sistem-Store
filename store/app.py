from flask import Flask, redirect, render_template, request, flash, url_for, g
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

import flask_login






from store.extensions import db, login_manager

from store.blueprints.login.views.LoginView import authentication
from store.blueprints.homepage.views.Homepage import  homepage
from store.blueprints.users.views.UsersView import users
from store.blueprints.tasks.views.TaskView import tasks
from store.blueprints.stores_management.view.StoreView import store
from store.blueprints.articles.views.ArticlesView import articles
from store.blueprints.production.views.ProductionView import production
from store.blueprints.stock.views.StockView import stock
from store.blueprints.daily_tasks.views.DailyView import daily_tasks


from datetime import datetime

def create_app():

    app = Flask(__name__)
    
    app.secret_key = b'2222'

    app.config.from_object('CONFIG')


    app.register_blueprint(authentication)
    app.register_blueprint(homepage)
    app.register_blueprint(tasks)
    app.register_blueprint(store)
    app.register_blueprint(users)
    app.register_blueprint(articles)
    app.register_blueprint(production)
    app.register_blueprint(stock)
    app.register_blueprint(daily_tasks)



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

    @app.context_processor
    def inject_today_date():
        return {'today_date': datetime.now().strftime("%Y-%m-%d")}
    
    @app.before_request
    def set_date():
        g.date = request.args.get('date') or datetime.now().strftime("%Y-%m-%d")


    return app
