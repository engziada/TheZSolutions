import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'your-salt-here'
    
    # Database
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(BASE_DIR, 'zsolutions.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///zsolutions.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folders
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    RESUMES_FOLDER = os.getenv('RESUMES_FOLDER', os.path.join(UPLOAD_FOLDER, 'resumes'))
    PROJECT_FILES_FOLDER = os.getenv('PROJECT_FILES_FOLDER', os.path.join(UPLOAD_FOLDER, 'project_files'))
    LOG_FOLDER = os.path.join(BASE_DIR, 'logs')
    
    # Ensure upload directories exist
    os.makedirs(RESUMES_FOLDER, exist_ok=True)
    os.makedirs(PROJECT_FILES_FOLDER, exist_ok=True)
    os.makedirs(LOG_FOLDER, exist_ok=True)
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  # 64MB max file size for all requests
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'doc', 'docx'}
    ALLOWED_PROJECT_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'zip', 'rar', '7z', 'png', 'jpg', 'jpeg'}
    
    # Email Configuration (Office 365)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.office365.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('The Z Solutions', os.environ.get('MAIL_USERNAME'))
    ADMIN_EMAIL = os.environ.get('MAIL_USERNAME')
    
    # Babel configuration
    LANGUAGES = ['en', 'ar']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # ReCAPTCHA Configuration
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'size': 'normal'}
    
    # Rate Limiting with in-memory storage
    # RATELIMIT_DEFAULT = "1 per hour"  # Removed default rate limit
    RATELIMIT_STORAGE_URL = "memory://"  # Use in-memory storage instead of Redis
    RATELIMIT_HEADERS_ENABLED = True
