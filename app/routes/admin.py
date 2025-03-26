from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, current_app
from app.models.application import Application
from app.models.project_request import ProjectRequest, ProjectRequestFile
from app.decorators import admin_required
from app import db
import os
from flask_babel import _
from app.models.user import User
from app.models.project import Project

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    stats = {
        # Applications Stats
        'total_applications': Application.query.count(),
        'pending_applications': Application.query.filter_by(status='pending').count(),
        'reviewing_applications': Application.query.filter_by(status='reviewing').count(),
        'accepted_applications': Application.query.filter_by(status='accepted').count(),
        'rejected_applications': Application.query.filter_by(status='rejected').count(),
        
        # Project Requests Stats
        'total_requests': ProjectRequest.query.count(),
        'pending_requests': ProjectRequest.query.filter_by(status='pending').count(),
        'reviewing_requests': ProjectRequest.query.filter_by(status='reviewing').count(),
        'accepted_requests': ProjectRequest.query.filter_by(status='accepted').count(),
        'rejected_requests': ProjectRequest.query.filter_by(status='rejected').count(),
        
        # User Stats
        'total_users': User.query.count(),
        'total_customers': User.query.filter_by(role='customer').count(),
        'total_developers': User.query.filter_by(role='developer').count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        
        # Project Stats
        'total_projects': Project.query.count(),
        'active_projects': Project.query.filter_by(status='active').count(),
        'completed_projects': Project.query.filter_by(status='completed').count()
    }
    
    recent_applications = Application.query.order_by(Application.application_date.desc()).limit(5).all()
    recent_requests = ProjectRequest.query.order_by(ProjectRequest.created_at.desc()).limit(5).all()
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_applications=recent_applications,
                         recent_requests=recent_requests,
                         recent_projects=recent_projects)

@admin_bp.route('/applications')
@admin_required
def applications():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    search_query = request.args.get('search', '')
    
    query = Application.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    # Apply search filter if search query is provided
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Application.first_name.ilike(search_term),
                Application.last_name.ilike(search_term),
                Application.email.ilike(search_term),
                Application.position.ilike(search_term),
                Application.skills.ilike(search_term)
            )
        )
    
    applications = query.order_by(Application.application_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('admin/applications.html', 
                         applications=applications,
                         current_status=status,
                         search_query=search_query,
                         min=min)

@admin_bp.route('/application/<int:id>')
@admin_required
def application_detail(id):
    application = Application.query.get_or_404(id)
    return render_template('admin/application_detail.html', application=application)

@admin_bp.route('/project-requests')
@admin_required
def project_requests():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = ProjectRequest.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    requests = query.order_by(ProjectRequest.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('admin/project_requests.html', 
                         requests=requests,
                         current_status=status)

@admin_bp.route('/project-request/<int:id>')
@admin_required
def request_detail(id):
    request = ProjectRequest.query.get_or_404(id)
    return render_template('admin/request_detail.html', request=request)

@admin_bp.route('/download/project-file/<int:file_id>')
@admin_required
def download_project_file(file_id):
    project_file = ProjectRequestFile.query.get_or_404(file_id)
    
    file_path = os.path.join(current_app.config['PROJECT_FILES_FOLDER'], project_file.filename)
    
    if not os.path.exists(file_path):
        flash(_('File not found.'), 'error')
        return redirect(url_for('admin.request_detail', id=project_file.request_id))
    
    try:
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        flash(_('Invalid file access attempt.'), 'error')
        return redirect(url_for('admin.request_detail', id=project_file.request_id))

@admin_bp.route('/application/<int:id>/update-status', methods=['POST'])
@admin_required
def update_application_status(id):
    application = Application.query.get_or_404(id)
    status = request.form.get('status')
    
    if status not in ['pending', 'reviewing', 'accepted', 'rejected']:
        return {'error': 'Invalid status'}, 400
    
    application.status = status
    db.session.commit()

    try:
        if status == 'rejected':
            from app.utils.email import send_application_rejection
            send_application_rejection(application)
        elif status == 'accepted':
            from app.utils.email import send_application_shortlisted
            send_application_shortlisted(application)
    except Exception as e:
        current_app.logger.error(f"Failed to send application status email: {str(e)}")
        # Don't return error to client, as the status update was successful
    
    return {'status': 'success'}, 200

@admin_bp.route('/project-request/<int:id>/update-status', methods=['POST'])
@admin_required
def update_request_status(id):
    project_request = ProjectRequest.query.get_or_404(id)
    status = request.form.get('status')
    
    if status not in ['pending', 'reviewing', 'accepted', 'rejected']:
        return {'error': 'Invalid status'}, 400
    
    project_request.status = status
    db.session.commit()
    
    return {'status': 'success'}, 200
