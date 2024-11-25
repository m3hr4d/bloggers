from flask import Flask, render_template
from flask_login import current_user
import os
from dotenv import load_dotenv
from email_func_app.extensions import db, login_manager, migrate, csrf
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    
    # File upload settings
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, os.getenv('UPLOAD_FOLDER', 'uploads'))
    
    # Security settings
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to False for development
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = int(os.getenv('REMEMBER_COOKIE_DURATION', 2592000))
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Configure logging
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Configure the logging system
    file_handler = RotatingFileHandler('logs/email_func_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Email Func App startup')

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import models
    from email_func_app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from email_func_app.blueprints.main import main as main_blueprint
    from email_func_app.routes.auth import auth_bp as auth_blueprint
    from email_func_app.blueprints.admin import admin as admin_blueprint
    from email_func_app.blueprints.offers import offers as offers_blueprint
    from email_func_app.routes.chat import chat as chat_blueprint
    from email_func_app.routes.plans import bp as plans_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(offers_blueprint, url_prefix='/offers')
    app.register_blueprint(chat_blueprint, url_prefix='/chat')
    app.register_blueprint(plans_blueprint)
    
    # Register the context processor for unread messages
    @app.context_processor
    def inject_unread_messages():
        """Add unread_messages count to all template contexts."""
        unread_messages = 0
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            try:
                from email_func_app.models import Message
                unread_messages = Message.query.filter_by(
                    recipient_id=current_user.id,
                    read=False
                ).count()
            except Exception as e:
                print(f"Error counting unread messages: {str(e)}")
                unread_messages = 0
        return dict(unread_messages=unread_messages)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app
