from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app.models.application import ProjectRequest, ProjectRequestFile
from app.utils.email import send_project_request_confirmation, send_project_request_notification
from app import db
import os
from datetime import datetime

requests_bp = Blueprint('requests', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_PROJECT_FILE_EXTENSIONS']

def save_project_files(files, project_request_id):
    """Save project files and return list of saved files"""
    saved_files = []
    for file in files:
        if file and allowed_file(file.filename):
            # Create a filename with timestamp to avoid duplicates
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"project_request_{project_request_id}_{timestamp}_{secure_filename(file.filename)}"
            
            # Use relative path for database storage
            relative_path = os.path.join('project_files', filename)
            
            # Get absolute path for file saving
            absolute_path = os.path.join(current_app.config['PROJECT_FILES_FOLDER'], filename)
            
            # Save the file
            file.save(absolute_path)
            
            # Create file record
            project_file = ProjectRequestFile(
                project_request_id=project_request_id,
                filename=filename,
                file_path=relative_path,
                file_type=filename.rsplit('.', 1)[1].lower()
            )
            db.session.add(project_file)
            saved_files.append(project_file)
            
    return saved_files

@requests_bp.route('/new', methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        try:
            # Get form data
            data = {
                'project_name': request.form.get('project_name'),
                'project_type': request.form.get('project_type'),
                'description': request.form.get('description'),
                'features': request.form.get('features'),
                'timeline': request.form.get('timeline'),
                'budget_range': request.form.get('budget'),
                'contact_name': request.form.get('contact_name'),
                'company_name': request.form.get('company'),
                'contact_email': request.form.get('contact_email'),
                'contact_phone': request.form.get('contact_phone'),
                'preferred_contact': request.form.get('preferred_contact', 'email'),
                'additional_info': request.form.get('additional_info'),
                'status': 'pending',
                'submission_date': datetime.utcnow()
            }
            
            # Validate required fields
            required_fields = ['project_name', 'project_type', 'description', 'features', 
                             'timeline', 'budget_range', 'contact_name', 'contact_email', 
                             'contact_phone']
            
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                flash(f'Please fill in all required fields: {", ".join(missing_fields)}', 'error')
                return redirect(url_for('requests.new_request'))
            
            # Create project request
            project_request = ProjectRequest(**data)
            db.session.add(project_request)
            db.session.commit()
            
            # Handle file uploads
            saved_files = []
            if 'files[]' in request.files:
                files = request.files.getlist('files[]')
                if files:
                    saved_files = save_project_files(files, project_request.id)
                    db.session.commit()
            
            # Log successful request
            current_app.logger.info(f'New project request received from {data["contact_name"]}')
            
            # Send email notifications
            try:
                send_project_request_confirmation(project_request)
                send_project_request_notification(project_request, saved_files)
            except Exception as e:
                current_app.logger.error(f'Error sending project request emails: {str(e)}')
                # Don't rollback the request if emails fail
            
            flash('Your project request has been submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('main.home'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error submitting project request: {str(e)}')
            flash('An error occurred while submitting your project request. Please try again.', 'error')
            return redirect(url_for('requests.new_request'))
    
    return render_template('requests/new.html', title='Submit Your Project Request')
