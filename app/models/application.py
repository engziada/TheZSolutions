from app import db
from datetime import datetime

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    years_of_experience = db.Column(db.Integer)
    skills = db.Column(db.JSON)  # List of skills
    portfolio_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    linkedin_url = db.Column(db.String(200))
    resume_path = db.Column(db.String(200))  # Path to uploaded resume
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Admin notes
    admin_notes = db.Column(db.Text)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_by = db.relationship('User', backref='reviewed_applications')

class ProjectRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # web, mobile, desktop, etc.
    budget_min = db.Column(db.Float)
    budget_max = db.Column(db.Float)
    timeline = db.Column(db.String(50))  # expected timeline
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    status = db.Column(db.String(20), default='new')  # new, reviewing, approved, rejected
    
    # Client information
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    client_phone = db.Column(db.String(20))
    company_name = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Admin fields
    admin_notes = db.Column(db.Text)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_by = db.relationship('User', backref='reviewed_requests')
    
    # Attachments
    attachments = db.relationship('ProjectRequestAttachment', backref='project_request', lazy=True)

class ProjectRequestAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_request_id = db.Column(db.Integer, db.ForeignKey('project_request.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
