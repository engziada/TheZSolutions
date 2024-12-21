from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app.models.application import JobApplication
from app import db
import os
from datetime import datetime

careers_bp = Blueprint('careers', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_RESUME_EXTENSIONS']

def save_resume(file, applicant_name):
    """Save resume file with proper naming and return the relative path"""
    if file and allowed_file(file.filename):
        # Create a filename with timestamp to avoid duplicates
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{applicant_name}_{timestamp}_{secure_filename(file.filename)}"
        
        # Use relative path for database storage
        relative_path = os.path.join('resumes', filename)
        
        # Get absolute path for file saving
        absolute_path = os.path.join(current_app.config['RESUMES_FOLDER'], filename)
        
        # Save the file
        file.save(absolute_path)
        
        return relative_path
    return None

@careers_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'position': request.form.get('position'),
                'years_of_experience': int(request.form.get('experience', 0)),
                'skills': request.form.get('skills'),
                'portfolio_url': request.form.get('portfolio'),
                'github_url': request.form.get('github'),
                'cover_letter': request.form.get('cover_letter', ''),  # Optional
                'status': 'pending',
                'application_date': datetime.utcnow()
            }
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'phone', 'position', 'skills']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                flash(f'Please fill in all required fields: {", ".join(missing_fields)}', 'error')
                return redirect(url_for('careers.apply'))
            
            # Handle resume upload
            if 'resume' not in request.files:
                flash('Resume file is required', 'error')
                return redirect(url_for('careers.apply'))
            
            file = request.files['resume']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('careers.apply'))
            
            # Save resume and get relative path
            applicant_name = f"{data['first_name']}_{data['last_name']}"
            resume_path = save_resume(file, applicant_name)
            
            if not resume_path:
                flash('Please upload a valid resume file (PDF, DOC, DOCX)', 'error')
                return redirect(url_for('careers.apply'))
            
            data['resume_path'] = resume_path
            
            # Create application
            application = JobApplication(**data)
            db.session.add(application)
            db.session.commit()
            
            # Log successful application
            current_app.logger.info(f'New job application received from {applicant_name}')
            
            flash('Your application has been submitted successfully! We will review it and get back to you soon.', 'success')
            return redirect(url_for('main.home'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error submitting job application: {str(e)}')
            flash('An error occurred while submitting your application. Please try again.', 'error')
            return redirect(url_for('careers.apply'))
    
    return render_template('careers/apply.html', title='Join Our Development Team')
