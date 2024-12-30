from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_from_directory, current_app
from flask_login import login_required, current_user
from app.models.user import User
from app.models.project import Project
from app.models.application import JobApplication, ProjectRequest, ProjectRequestFile
from app import db
from datetime import datetime
from sqlalchemy import func, or_
import logging.handlers
import os
from logging.handlers import RotatingFileHandler
from app.utils.email import (
    send_application_rejection, 
    send_application_shortlisted, 
    send_project_request_rejection,
    send_project_request_approval
)

admin_bp = Blueprint('admin', __name__)

# Configure logging with thread-safe rotating file handler
def configure_logging():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, 'admin.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Use a Queue handler to handle concurrent writes
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10240,
        backupCount=10,
        delay=True  # Delay file creation until first write
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Create logger with a unique name
    logger = logging.getLogger('admin.' + str(os.getpid()))
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    logger.addHandler(file_handler)
    
    return logger

# Create logger instance
logger = configure_logging()

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics
    stats = {
        'total_users': User.query.count(),
        'total_customers': User.query.filter_by(role='customer').count(),
        'total_developers': User.query.filter_by(role='developer').count(),
        'total_projects': Project.query.count(),
        'active_projects': Project.query.filter_by(status='active').count(),
        'pending_projects': Project.query.filter_by(status='pending').count(),
        'completed_projects': Project.query.filter_by(status='completed').count(),
        'pending_job_applications': JobApplication.query.filter_by(status='pending').count(),
        'pending_project_requests': ProjectRequest.query.filter_by(status='pending').count(),
    }
    
    # Get recent project requests
    recent_project_requests = ProjectRequest.query.order_by(ProjectRequest.submission_date.desc()).limit(5).all()
    
    # Get recent job applications
    recent_job_applications = JobApplication.query.order_by(JobApplication.application_date.desc()).limit(5).all()
    
    logger.info(f'Admin {current_user.email} accessed dashboard')
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         stats=stats,
                         recent_project_requests=recent_project_requests,
                         recent_job_applications=recent_job_applications)

@admin_bp.route('/project-requests')
@login_required
@admin_required
def project_requests():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    query = ProjectRequest.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                ProjectRequest.project_name.ilike(search_term),
                ProjectRequest.contact_name.ilike(search_term),
                ProjectRequest.contact_email.ilike(search_term)
            )
        )
    
    # Add proper ordering
    query = query.order_by(ProjectRequest.submission_date.desc())
    
    # Use Flask-SQLAlchemy's pagination
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    project_requests = pagination.items
    
    logger.info(f'Admin {current_user.email} accessed project requests list with status={status}')
    
    return render_template('admin/project_requests.html',
                         title='Project Requests',
                         project_requests=project_requests,
                         pagination=pagination,
                         current_status=status)

@admin_bp.route('/job-applications')
@login_required
@admin_required
def job_applications():
    status = request.args.get('status', 'all')
    search_skills = request.args.get('skills', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query
    query = JobApplication.query

    # Filter by status if specified
    if status != 'all':
        query = query.filter(JobApplication.status == status)

    # Search by skills if provided
    if search_skills:
        search_terms = search_skills.split()
        # Create a filter condition for each search term
        skill_filters = []
        for term in search_terms:
            skill_filters.append(JobApplication.skills.ilike(f'%{term}%'))
        # Combine filters with OR
        if skill_filters:
            query = query.filter(or_(*skill_filters))

    # Order by application date, newest first
    query = query.order_by(JobApplication.application_date.desc())

    # Paginate results
    applications = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin/job_applications.html',
                         title='Job Applications',
                         applications=applications,
                         current_status=status,
                         current_skills=search_skills)

@admin_bp.route('/project-request/<int:request_id>')
@login_required
@admin_required
def view_project_request(request_id):
    project_request = ProjectRequest.query.get_or_404(request_id)
    logger.info(f'Admin {current_user.email} viewed project request {project_request.project_name}')
    
    return render_template('admin/project_request_detail.html',
                         title=f'Project Request - {project_request.project_name}',
                         project_request=project_request)

@admin_bp.route('/job-application/<int:application_id>')
@login_required
@admin_required
def view_job_application(application_id):
    application = JobApplication.query.get_or_404(application_id)
    logger.info(f'Admin {current_user.email} viewed job application from {application.first_name} {application.last_name}')
    
    return render_template('admin/job_application_detail.html',
                         title=f'Job Application - {application.first_name} {application.last_name}',
                         application=application)

@admin_bp.route('/job-application/<int:application_id>/download-cv')
@login_required
@admin_required
def download_cv(application_id):
    application = JobApplication.query.get_or_404(application_id)
    if not application.resume_path:
        flash('No CV file found for this application.', 'error')
        return redirect(url_for('admin.view_job_application', application_id=application_id))
    
    # Get the resumes folder from config
    resumes_folder = current_app.config['RESUMES_FOLDER']
    
    # Log the download
    logger.info(f'Admin {current_user.email} downloaded CV for application from {application.first_name} {application.last_name}')
    
    return send_from_directory(
        resumes_folder,
        os.path.basename(application.resume_path),
        as_attachment=True,
        download_name=f'CV_{application.first_name}_{application.last_name}{os.path.splitext(application.resume_path)[1]}'
    )

@admin_bp.route('/project-request/<int:request_id>/download-document/<int:file_id>')
@login_required
@admin_required
def download_project_document(request_id, file_id):
    project_request = ProjectRequest.query.get_or_404(request_id)
    project_file = ProjectRequestFile.query.get_or_404(file_id)
    
    if project_file.project_request_id != request_id:
        flash('Invalid file access attempt.', 'error')
        return redirect(url_for('admin.view_project_request', request_id=request_id))
    
    # Get the documents folder path
    documents_folder = os.path.join(current_app.root_path, 'uploads', 'project_files')
    
    # Log the download
    logger.info(f'Admin {current_user.email} downloaded document {project_file.filename} for project request {project_request.project_name}')
    
    return send_from_directory(
        documents_folder,
        os.path.basename(project_file.file_path),
        as_attachment=True,
        download_name=project_file.filename
    )

@admin_bp.route('/project-request/<int:request_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_project_request_status(request_id):
    project_request = ProjectRequest.query.get_or_404(request_id)
    
    # Log the incoming request data for debugging
    logger.info(f'Received status update request. Form data: {request.form}')
    logger.info(f'Request content type: {request.content_type}')
    
    # Try both form and json data
    new_status = request.form.get('status')
    if not new_status and request.is_json:
        new_status = request.json.get('status')
    
    if not new_status:
        logger.error('No status provided in request')
        return jsonify({'error': 'No status provided'}), 400
    
    if new_status not in ['pending', 'approved', 'rejected']:
        logger.error(f'Invalid status provided: {new_status}')
        return jsonify({'error': 'Invalid status'}), 400
    
    old_status = project_request.status
    project_request.status = new_status
    
    try:
        db.session.commit()
        
        # Send appropriate email based on status change
        if old_status != new_status:
            try:
                if new_status == 'rejected':
                    logger.info(f'Attempting to send rejection email for project request {project_request.project_name}')
                    send_project_request_rejection(project_request)
                    logger.info(f'Successfully sent rejection email for project request {project_request.project_name}')
                elif new_status == 'approved':
                    logger.info(f'Attempting to send approval email for project request {project_request.project_name}')
                    send_project_request_approval(project_request)
                    logger.info(f'Successfully sent approval email for project request {project_request.project_name}')
            except Exception as e:
                logger.error(f'Failed to send email for project request {project_request.project_name}: {str(e)}')
                # Don't return error to user, as the status update was successful
        
        logger.info(f'Admin {current_user.email} updated project request {project_request.project_name} status from {old_status} to {new_status}')
        return jsonify({'message': 'Status updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating project request status: {str(e)}')
        return jsonify({'error': 'Failed to update status'}), 500

@admin_bp.route('/job-application/<int:application_id>/update-status', methods=['POST'])
@login_required
@admin_required
def update_job_application_status(application_id):
    try:
        application = JobApplication.query.get_or_404(application_id)
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['pending', 'shortlisted', 'rejected']:
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        
        application.status = new_status
        
        # Send appropriate email based on status
        if new_status == 'rejected':
            try:
                send_application_rejection(application)
            except Exception as e:
                logger.error(f'Failed to send rejection email: {str(e)}')
                # Continue with status update even if email fails
        elif new_status == 'shortlisted':
            try:
                send_application_shortlisted(application)
            except Exception as e:
                logger.error(f'Failed to send shortlist notification email: {str(e)}')
                # Continue with status update even if email fails
        
        db.session.commit()
        logger.info(f'Job application {application_id} status updated to {new_status} by admin {current_user.email}')
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating job application status: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500
