from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # MariaDB configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mariadbb:z8YiBYNfHneqAB9NqJSJX9xqn5GB@localhost/mariadbb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False  # Temporarily disable CSRF for development

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'لطفاً وارد حساب کاربری خود شوید.'
    login_manager.login_message_category = 'info'

    from email_func_app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from email_func_app.main.routes import main
    app.register_blueprint(main)

    from email_func_app.auth.routes import auth
    app.register_blueprint(auth)

    from email_func_app.offers.routes import offers
    app.register_blueprint(offers, url_prefix='/offers')

    return app
