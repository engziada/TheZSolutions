from app import create_app, db
from dotenv import load_dotenv
import os
from app.models.user import User

load_dotenv()
application = create_app()  # This is the WSGI application

def create_folders():
    """Create necessary folders if they don't exist"""
    folders = ['logs', 'checkpoints', 'uploads']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            application.logger.info(f'Created {folder} directory')

def create_default_admin():
    """Create default admin user if it doesn't exist"""
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@thez.solutions')
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'TheZSolutions2024!')
    
    # Check if admin exists
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            username=admin_username,
            role='admin',
            is_active=True
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        application.logger.info('Created default admin user')
    else:
        application.logger.info('Default admin user already exists')

# Create the folders and initialize the database
with application.app_context():
    create_folders()
    db.create_all()
    create_default_admin()

# For local development
if __name__ == '__main__':
    application.run(debug=True)

# For Gunicorn
app = application
