from app import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import mimetypes

class ProjectRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    timeline = db.Column(db.String(50))
    features = db.Column(db.Text, nullable=True)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    preferred_contact = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='project_requests')
    files = db.relationship('ProjectRequestFile', backref='project_request', lazy='dynamic')
    
    def __repr__(self):
        return f'<ProjectRequest {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'category': self.category,
            'status': self.status,
            'budget_min': self.budget_min,
            'budget_max': self.budget_max,
            'timeline': self.timeline,
            'features': self.features,
            'contact_name': self.contact_name,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'preferred_contact': self.preferred_contact,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ProjectRequestFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_request_id = db.Column(db.Integer, db.ForeignKey('project_request.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, project_request_id, file):
        self.project_request_id = project_request_id
        self.original_filename = file.filename
        self.filename = secure_filename(file.filename)
        
        # Get file size
        file.seek(0, os.SEEK_END)
        self.file_size = file.tell()
        file.seek(0)
        
        # Determine MIME type
        self.mime_type = mimetypes.guess_type(self.filename)[0]
        
        # Set file type based on extension
        _, ext = os.path.splitext(self.filename)
        self.file_type = ext.lower()[1:] if ext else None
        
        # Set file path relative to upload directory
        self.file_path = os.path.join(
            'uploads',
            'requests',
            str(self.project_request_id),
            self.filename
        )
    
    def __repr__(self):
        return f'<ProjectRequestFile {self.filename}>'
    
    def get_absolute_path(self):
        return os.path.abspath(self.file_path)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_request_id': self.project_request_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
