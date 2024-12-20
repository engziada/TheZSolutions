from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import mimetypes

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_profile.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requirements = db.relationship('ProjectRequirement', backref='project', lazy='dynamic')
    milestones = db.relationship('ProjectMilestone', backref='project', lazy='dynamic')
    files = db.relationship('ProjectFile', backref='project', lazy='dynamic')
    
    def __repr__(self):
        return f'<Project {self.title}>'

class ProjectRequirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20))  # high, medium, low
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProjectMilestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    payment_amount = db.Column(db.Float)
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, processing, paid

class ProjectFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)  # Size in bytes
    mime_type = db.Column(db.String(100))
    category = db.Column(db.String(50))  # document, image, source_code, etc.
    version = db.Column(db.Integer, default=1)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    download_count = db.Column(db.Integer, default=0)
    last_downloaded_at = db.Column(db.DateTime)
    
    # Relationships
    uploader = db.relationship('User', backref='uploaded_files')
    
    def __init__(self, project_id, file, uploaded_by, description=None, category=None, is_public=False):
        self.project_id = project_id
        self.original_filename = file.filename
        self.filename = secure_filename(file.filename)
        self.uploaded_by = uploaded_by
        self.description = description
        self.category = category
        self.is_public = is_public
        
        # Get file size
        file.seek(0, os.SEEK_END)
        self.file_size = file.tell()
        file.seek(0)
        
        # Determine MIME type
        self.mime_type = mimetypes.guess_type(self.filename)[0]
        
        # Set file type based on extension
        _, ext = os.path.splitext(self.filename)
        self.file_type = ext.lower()[1:] if ext else None
        
        # Generate unique filename with version
        base_name, ext = os.path.splitext(self.filename)
        self.filename = f"{base_name}_v{self.version}{ext}"
        
        # Set file path relative to upload directory
        self.file_path = os.path.join(
            'uploads',
            'projects',
            str(self.project_id),
            self.category if self.category else '',
            self.filename
        )
    
    def increment_version(self):
        """Increment file version and update filename"""
        self.version += 1
        base_name, ext = os.path.splitext(self.original_filename)
        self.filename = f"{base_name}_v{self.version}{ext}"
        self.file_path = os.path.join(
            'uploads',
            'projects',
            str(self.project_id),
            self.category if self.category else '',
            self.filename
        )
    
    def increment_download_count(self):
        """Increment download count and update last downloaded timestamp"""
        self.download_count += 1
        self.last_downloaded_at = datetime.utcnow()
        db.session.commit()
    
    def get_absolute_path(self):
        """Get absolute file path"""
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', self.file_path)
    
    def to_dict(self):
        """Convert file object to dictionary"""
        return {
            'id': self.id,
            'filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'category': self.category,
            'version': self.version,
            'uploaded_by': self.uploader.username,
            'uploaded_at': self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S'),
            'description': self.description,
            'is_public': self.is_public,
            'download_count': self.download_count,
            'last_downloaded_at': self.last_downloaded_at.strftime('%Y-%m-%d %H:%M:%S') if self.last_downloaded_at else None
        }

# Association table for many-to-many relationship between projects and developers
project_developers = db.Table('project_developers',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('developer_id', db.Integer, db.ForeignKey('developer_profile.id'), primary_key=True)
)
