from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app.models.application import JobApplication
from app import db
import os
from datetime import datetime

careers_bp = Blueprint('careers', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@careers_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # Get form data
        data = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'years_of_experience': int(request.form.get('years_of_experience', 0)),
            'skills': request.form.getlist('skills[]'),
            'portfolio_url': request.form.get('portfolio_url'),
            'github_url': request.form.get('github_url'),
            'linkedin_url': request.form.get('linkedin_url'),
            'cover_letter': request.form.get('cover_letter')
        }
        
        # Handle resume upload
        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'resumes', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                data['resume_path'] = filepath
        
        # Create application
        application = JobApplication(**data)
        db.session.add(application)
        db.session.commit()
        
        flash('Your application has been submitted successfully!', 'success')
        return redirect(url_for('careers.apply'))
    
    return render_template('careers/apply.html', title='Apply as Developer')
