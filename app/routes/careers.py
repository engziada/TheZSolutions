from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.models.application import Application
from app.utils.email import send_application_notification
from app import db
import os
from werkzeug.utils import secure_filename
from flask_babel import _

careers_bp = Blueprint('careers', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_RESUME_EXTENSIONS']

@careers_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            # Get form data
            required_fields = [
                'first_name', 'last_name', 'email', 'phone',
                'position', 'experience', 'skills'
            ]
            
            # Check required fields
            missing_fields = [field for field in required_fields if not request.form.get(field)]
            if missing_fields:
                flash(_('Please fill in all required fields: %s') % ', '.join(missing_fields), 'error')
                return redirect(url_for('careers.apply'))
            
            # Check if resume was uploaded
            if 'resume' not in request.files:
                flash(_('Resume file is required'), 'error')
                return redirect(url_for('careers.apply'))
            
            file = request.files['resume']
            if file.filename == '':
                flash(_('No file selected'), 'error')
                return redirect(url_for('careers.apply'))
            
            if file and allowed_file(file.filename):
                # Save resume file
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['RESUMES_FOLDER'], filename)
                file.save(file_path)
                
                # Create application record
                application = Application(
                    first_name=request.form['first_name'],
                    last_name=request.form['last_name'],
                    email=request.form['email'],
                    phone=request.form['phone'],
                    position=request.form['position'],
                    experience=request.form['experience'],
                    skills=request.form['skills'],
                    portfolio_url=request.form.get('portfolio'),
                    github_url=request.form.get('github'),
                    cover_letter=request.form.get('cover_letter'),
                    resume_path=filename,
                    status='pending'
                )
                
                db.session.add(application)
                db.session.commit()
                
                # Send email notifications
                if send_application_notification(application):
                    flash(_('Your application has been submitted successfully! We will review it and get back to you soon.'), 'success')
                else:
                    flash(_('Your application was received but there was an issue sending the notification. Our team will still contact you soon.'), 'warning')
                
                return redirect(url_for('main.home'))
            else:
                flash(_('Please upload a valid resume file (PDF, DOC, DOCX)'), 'error')
                return redirect(url_for('careers.apply'))
                
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error submitting application: {str(e)}')
            flash(_('An error occurred while submitting your application. Please try again.'), 'error')
            return redirect(url_for('careers.apply'))
    
    return render_template('careers/apply.html', title=_('Join Our Development Team'))
