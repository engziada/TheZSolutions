from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os

class PortfolioProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(length=16777215), nullable=False)  # Using MEDIUMTEXT for larger content
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='portfolio_projects')
    images = db.relationship('PortfolioImage', backref='project', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<PortfolioProject {self.title}>'

class PortfolioImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('portfolio_project.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, project_id, file, is_primary=False):
        self.project_id = project_id
        self.original_filename = file.filename
        self.filename = secure_filename(file.filename)
        self.is_primary = is_primary

        # Generate unique filename
        base_name, ext = os.path.splitext(self.filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        self.filename = f"{base_name}_{timestamp}{ext}"

        # Set file path relative to static directory with forward slashes
        self.file_path = '/'.join([
            'uploads',
            'portfolio',
            str(self.project_id),
            self.filename
        ])

    def __repr__(self):
        return f'<PortfolioImage {self.filename}>'
