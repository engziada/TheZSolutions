from app import create_app, db
from dotenv import load_dotenv
import os

load_dotenv()
app = create_app()

def create_folders():
    """Create necessary folders if they don't exist"""
    folders = ['logs', 'checkpoints', 'uploads']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            app.logger.info(f'Created {folder} directory')

if __name__ == '__main__':
    with app.app_context():
        create_folders()
        db.create_all()
    app.run(debug=True)
