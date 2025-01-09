from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_babel import Babel
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
import subprocess
from datetime import datetime
from .utils.babel import init_babel
from .cli import translate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

def compile_translations():
    """Compile translation files"""
    try:
        subprocess.run(['pybabel', 'compile', '-d', 'app/translations'])
    except Exception as e:
        print(f"Warning: Could not compile translations: {e}")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    # Initialize Babel and compile translations
    babel = init_babel(app)
    app.jinja_env.add_extension('jinja2.ext.i18n')
    compile_translations()  # Compile translations at startup

    # Register CLI commands
    app.cli.add_command(translate)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Setup logging
    file_handler = RotatingFileHandler('logs/zsolutions.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('The Z Solutions startup')

    # Add current year to all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.customer import customer_bp
    from app.routes.developer import developer_bp
    from app.routes.admin import admin_bp
    from app.routes.careers import careers_bp
    from app.routes.project_requests import requests_bp
    from app.routes.seo import seo_bp
    from app.routes.theme import theme_bp
    from app.routes.downloads import bp as downloads_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(developer_bp, url_prefix='/developer')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(careers_bp, url_prefix='/careers')
    app.register_blueprint(requests_bp, url_prefix='/requests')
    app.register_blueprint(seo_bp)
    app.register_blueprint(theme_bp)
    app.register_blueprint(downloads_bp, url_prefix='/downloads')

    from app.commands.create_admin import create_admin_command
    app.cli.add_command(create_admin_command)

    return app
