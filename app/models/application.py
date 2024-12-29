from app import db
from datetime import datetime

class JobApplication(db.Model):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    portfolio_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    resume_path = db.Column(db.String(255), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<JobApplication {self.first_name} {self.last_name}>'

class ProjectRequest(db.Model):
    __tablename__ = 'project_requests'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.Text, nullable=False)
    timeline = db.Column(db.String(20), nullable=False)
    budget_range = db.Column(db.String(20), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    preferred_contact = db.Column(db.String(10), nullable=False)
    additional_info = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProjectRequest {self.project_name}>'

class ProjectRequestFile(db.Model):
    __tablename__ = 'project_request_files'

    id = db.Column(db.Integer, primary_key=True)
    project_request_id = db.Column(db.Integer, db.ForeignKey('project_requests.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    project_request = db.relationship('ProjectRequest', backref='files')
    
    def __repr__(self):
        return f'<ProjectRequestFile {self.filename}>'
