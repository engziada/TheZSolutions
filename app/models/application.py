from app import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String(20), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    portfolio_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    cover_letter = db.Column(db.Text)
    resume_path = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='pending')
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Application {self.first_name} {self.last_name} - {self.position}>'
