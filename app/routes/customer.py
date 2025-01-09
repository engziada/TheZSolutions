from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models.project import Project, ProjectRequirement, ProjectFile
from app.models.user import CustomerProfile
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask_babel import _

customer_bp = Blueprint('customer', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'customer':
        flash(_('Access denied. Customer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    projects = Project.query.filter_by(customer_id=current_user.customer_profile.id).all()
    return render_template('customer/dashboard.html', 
                         title='Customer Dashboard',
                         projects=projects)

@customer_bp.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if current_user.role != 'customer':
        flash(_('Access denied. Customer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        budget_min = float(request.form.get('budget_min', 0))
        budget_max = float(request.form.get('budget_max', 0))
        
        project = Project(
            title=title,
            description=description,
            category=category,
            budget_min=budget_min,
            budget_max=budget_max,
            customer_id=current_user.customer_profile.id
        )
        
        # Handle requirements
        requirements = request.form.getlist('requirements[]')
        priorities = request.form.getlist('priorities[]')
        for req, priority in zip(requirements, priorities):
            if req:  # Only add non-empty requirements
                requirement = ProjectRequirement(
                    title=req,
                    priority=priority
                )
                project.requirements.append(requirement)
        
        # Handle file uploads
        if 'files[]' in request.files:
            files = request.files.getlist('files[]')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    project_file = ProjectFile(
                        filename=filename,
                        file_path=file_path,
                        file_type=filename.rsplit('.', 1)[1].lower(),
                        uploaded_by=current_user.id
                    )
                    project.files.append(project_file)
        
        db.session.add(project)
        db.session.commit()
        
        flash(_('Project created successfully!'), 'success')
        return redirect(url_for('customer.dashboard'))
    
    return render_template('customer/new_project.html', title='New Project')

@customer_bp.route('/project/<int:project_id>')
@login_required
def view_project(project_id):
    if current_user.role != 'customer':
        flash(_('Access denied. Customer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    project = Project.query.get_or_404(project_id)
    if project.customer_id != current_user.customer_profile.id:
        flash(_('Access denied. This project belongs to another customer.'), 'error')
        return redirect(url_for('customer.dashboard'))
    
    return render_template('customer/view_project.html',
                         title=f'Project: {project.title}',
                         project=project)

@customer_bp.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    if current_user.role != 'customer':
        flash(_('Access denied. Customer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    project = Project.query.get_or_404(project_id)
    if project.customer_id != current_user.customer_profile.id:
        flash(_('Access denied. This project belongs to another customer.'), 'error')
        return redirect(url_for('customer.dashboard'))
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.category = request.form.get('category')
        project.budget_min = float(request.form.get('budget_min', 0))
        project.budget_max = float(request.form.get('budget_max', 0))
        
        db.session.commit()
        flash(_('Project updated successfully!'), 'success')
        return redirect(url_for('customer.view_project', project_id=project.id))
    
    return render_template('customer/edit_project.html',
                         title=f'Edit Project: {project.title}',
                         project=project)

@customer_bp.route('/project/<int:project_id>/upload', methods=['POST'])
@login_required
def upload_file(project_id):
    if current_user.role != 'customer':
        flash(_('Access denied. Customer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    project = Project.query.get_or_404(project_id)
    if project.customer_id != current_user.customer_profile.id:
        flash(_('Access denied. This project belongs to another customer.'), 'error')
        return redirect(url_for('customer.dashboard'))
    
    if 'file' not in request.files:
        flash(_('No file selected'), 'error')
        return redirect(url_for('customer.view_project', project_id=project.id))
    
    file = request.files['file']
    if file.filename == '':
        flash(_('No file selected'), 'error')
        return redirect(url_for('customer.view_project', project_id=project.id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        project_file = ProjectFile(
            project_id=project.id,
            filename=filename,
            file_path=file_path,
            file_type=filename.rsplit('.', 1)[1].lower(),
            uploaded_by=current_user.id
        )
        
        db.session.add(project_file)
        db.session.commit()
        
        flash(_('File uploaded successfully!'), 'success')
    else:
        flash(_('Invalid file type'), 'error')
    
    return redirect(url_for('customer.view_project', project_id=project.id))
