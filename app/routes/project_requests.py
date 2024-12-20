from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app.models.application import ProjectRequest, ProjectRequestAttachment
from app import db
import os
from datetime import datetime

requests_bp = Blueprint('requests', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'zip'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@requests_bp.route('/new', methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        # Get form data
        data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'category': request.form.get('category'),
            'budget_min': float(request.form.get('budget_min', 0)),
            'budget_max': float(request.form.get('budget_max', 0)),
            'timeline': request.form.get('timeline'),
            'priority': request.form.get('priority', 'normal'),
            'client_name': request.form.get('client_name'),
            'client_email': request.form.get('client_email'),
            'client_phone': request.form.get('client_phone'),
            'company_name': request.form.get('company_name')
        }
        
        # Create project request
        project_request = ProjectRequest(**data)
        db.session.add(project_request)
        
        # Handle file attachments
        if 'attachments[]' in request.files:
            files = request.files.getlist('attachments[]')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'project_requests', str(project_request.id), filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    
                    attachment = ProjectRequestAttachment(
                        project_request=project_request,
                        filename=filename,
                        file_path=filepath,
                        file_type=filename.rsplit('.', 1)[1].lower()
                    )
                    db.session.add(attachment)
        
        db.session.commit()
        
        flash('Your project request has been submitted successfully! We will contact you soon.', 'success')
        return redirect(url_for('requests.new_request'))
    
    return render_template('requests/new.html', title='New Project Request')
