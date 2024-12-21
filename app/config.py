import os

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
    
    # Ensure upload directories exist
    os.makedirs(RESUMES_FOLDER, exist_ok=True)
    os.makedirs(PROJECT_FILES_FOLDER, exist_ok=True)
    
    # Maximum file size (5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    
    # Allowed file extensions
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'doc', 'docx'}
    ALLOWED_PROJECT_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'zip', 'rar', '7z'}
