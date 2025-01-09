from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.models.project_request import ProjectRequest, ProjectRequestFile
from app.utils.email import send_project_request_notification
from app import db
import os
from werkzeug.utils import secure_filename
from flask_babel import _

requests_bp = Blueprint('requests', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_PROJECT_FILE_EXTENSIONS']

@requests_bp.route('/new', methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        try:
            # Get form data
            required_fields = [
                'project_name', 'project_type', 'description', 'features',
                'timeline', 'budget', 'contact_name', 'contact_email',
                'contact_phone', 'preferred_contact'
            ]
            
            # Check required fields
            missing_fields = [field for field in required_fields if not request.form.get(field)]
            if missing_fields:
                flash(_('Please fill in all required fields: %s') % ', '.join(missing_fields), 'error')
                return redirect(url_for('requests.new_request'))
            
            # Parse budget range
            budget = request.form['budget']
            try:
                # Remove $ and commas, then split on hyphen
                budget_parts = budget.replace('$', '').replace(',', '').split('-')
                budget_min = float(budget_parts[0].strip())
                budget_max = float(budget_parts[1].strip()) if len(budget_parts) > 1 else budget_min
            except (ValueError, IndexError) as e:
                current_app.logger.error(f'Error parsing budget {budget}: {str(e)}')
                budget_min = 0
                budget_max = 0
            
            # Create project request
            project_request = ProjectRequest(
                title=request.form['project_name'],
                category=request.form['project_type'],
                description=request.form['description'],
                features=request.form['features'],
                timeline=request.form['timeline'],
                budget_min=budget_min,
                budget_max=budget_max,
                contact_name=request.form['contact_name'],
                contact_email=request.form['contact_email'],
                contact_phone=request.form['contact_phone'],
                preferred_contact=request.form['preferred_contact'],
                user_id=1  # Set a default user_id for now
            )
            
            db.session.add(project_request)
            db.session.flush()  # Get project_request.id before committing
            
            # Handle file uploads
            if 'files[]' in request.files:
                files = request.files.getlist('files[]')
                for file in files:
                    if file.filename != '' and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(current_app.config['PROJECT_FILES_FOLDER'], filename)
                        file.save(file_path)
                        
                        project_file = ProjectRequestFile(
                            project_request_id=project_request.id,
                            filename=filename,
                            original_filename=file.filename,
                            file_path=file_path,
                            file_type=filename.rsplit('.', 1)[1].lower(),
                            file_size=os.path.getsize(file_path),
                            mime_type=file.content_type if hasattr(file, 'content_type') else None
                        )
                        db.session.add(project_file)
            
            db.session.commit()
            
            # Send email notifications
            if send_project_request_notification(project_request):
                flash(_('Your project request has been submitted successfully! We will contact you soon.'), 'success')
            else:
                flash(_('Your project request was received but there was an issue sending the notification. Our team will still contact you soon.'), 'warning')
            
            return redirect(url_for('main.home'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error submitting project request: {str(e)}')
            flash(_('An error occurred while submitting your project request. Please try again.'), 'error')
            return redirect(url_for('requests.new_request'))
    
    return render_template('requests/new.html', title=_('Submit Your Project Request'))
