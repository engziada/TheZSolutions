import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'zsolutions.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Upload folders
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    RESUMES_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    PROJECT_FILES_FOLDER = os.path.join(UPLOAD_FOLDER, 'project_files')
    LOG_FOLDER = os.path.join(BASE_DIR, 'Log')
    
    # Ensure upload directories exist
    os.makedirs(RESUMES_FOLDER, exist_ok=True)
    os.makedirs(PROJECT_FILES_FOLDER, exist_ok=True)
    os.makedirs(LOG_FOLDER, exist_ok=True)
    
    # Maximum file size (5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    
    # Allowed file extensions
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'doc', 'docx'}
    ALLOWED_PROJECT_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'zip', 'rar', '7z'}
    
    # Email Configuration (Office 365)
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Using the existing email address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Using the Office 365 password
    MAIL_DEFAULT_SENDER = ('The Z Solutions', os.environ.get('MAIL_USERNAME'))
    ADMIN_EMAIL = os.environ.get('MAIL_USERNAME')
