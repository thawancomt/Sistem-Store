from flask import Flask, redirect, render_template, request, flash, url_for, g
from werkzeug.middleware.proxy_fix import ProxyFix

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_fresh
from flask_migrate import Migrate

from store.micro_services.code_verification import CodeModel



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
from store.blueprints.product_shelf_life.views.ShelfLifeView import shelf_life
from store.blueprints.providers.views.ProvidersView import providers

from store.blueprints.create_order.views.CreateOrder import CreateOrderBlueprint

# TEST
from store.blueprints.profile_image.view import profile_image

# First Run
from store.first_run import check_store, check_user



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
    app.register_blueprint(profile_image)
    app.register_blueprint(shelf_life)
    app.register_blueprint(providers)
    app.register_blueprint(CreateOrderBlueprint)



    migrate = Migrate(app, db)

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

        check_store()
        check_user()
        
    login_manager.init_app(app)
    login_manager.refresh_view = 'auth.login'
    login_manager.needs_refresh_message = 'Please insert your credentials again to confirm the login'
    
    migrate.init_app(app, db)
    


    
    

    @app.route('/')
    def home():
        return redirect(url_for('homepage.home'))
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('/error/404.html'), 404

    @app.context_processor
    def inject_today_date():
        return {'today_date': datetime.now().strftime("%Y-%m-%d"),
                'fresh_user': login_fresh}
    
    @app.before_request
    def set_date():
        
        g.date = request.args.get('date') or datetime.now().strftime("%Y-%m-%d")
        
        


    return app
