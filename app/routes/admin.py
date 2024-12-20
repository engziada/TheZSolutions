from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.user import User, CustomerProfile, DeveloperProfile
from app.models.project import Project, ProjectMilestone
from app.models.content import TeamMember, Service, Testimonial
from app.utils.email import (send_welcome_email, send_project_assigned_email,
                           send_project_status_update_email, send_project_completed_email,
                           send_milestone_completed_email)
from app import db
from datetime import datetime
from sqlalchemy import func
import json

admin_bp = Blueprint('admin', __name__)

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
    }
    
    # Get recent projects
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         stats=stats,
                         recent_projects=recent_projects,
                         recent_users=recent_users)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    role = request.args.get('role', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = User.query
    if role != 'all':
        query = query.filter_by(role=role)
    
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/users.html',
                         title='User Management',
                         users=users,
                         current_role=role)

@admin_bp.route('/users/toggle/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    if user.is_active:
        send_welcome_email(user)
    
    return jsonify({'status': 'success', 'message': f'User {status} successfully!'})

@admin_bp.route('/projects')
@login_required
@admin_required
def projects():
    status = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = Project.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    projects = query.order_by(Project.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return render_template('admin/projects.html',
                         title='Project Management',
                         projects=projects,
                         current_status=status)

@admin_bp.route('/project/<int:project_id>')
@login_required
@admin_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    available_developers = DeveloperProfile.query.filter_by(availability_status='available').all()
    
    return render_template('admin/view_project.html',
                         title=f'Project: {project.title}',
                         project=project,
                         available_developers=available_developers)

@admin_bp.route('/project/<int:project_id>/assign', methods=['POST'])
@login_required
@admin_required
def assign_developer(project_id):
    project = Project.query.get_or_404(project_id)
    developer_id = request.form.get('developer_id')
    
    if not developer_id:
        flash('Please select a developer.', 'error')
        return redirect(url_for('admin.view_project', project_id=project.id))
    
    developer = DeveloperProfile.query.get_or_404(developer_id)
    
    if developer in project.developers:
        flash('Developer is already assigned to this project.', 'error')
    else:
        project.developers.append(developer)
        project.status = 'active'
        db.session.commit()
        
        # Send email notifications
        send_project_assigned_email(project, developer)
        send_project_status_update_email(project)
        
        flash('Developer assigned successfully!', 'success')
    
    return redirect(url_for('admin.view_project', project_id=project.id))

@admin_bp.route('/project/<int:project_id>/milestones')
@login_required
@admin_required
def project_milestones(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('admin/milestones.html', project=project)

@admin_bp.route('/milestone/<int:milestone_id>')
@login_required
@admin_required
def get_milestone(milestone_id):
    milestone = ProjectMilestone.query.get_or_404(milestone_id)
    return jsonify({
        'id': milestone.id,
        'title': milestone.title,
        'description': milestone.description,
        'due_date': milestone.due_date.strftime('%Y-%m-%d') if milestone.due_date else None,
        'payment_amount': milestone.payment_amount
    })

@admin_bp.route('/milestone/add', methods=['POST'])
@login_required
@admin_required
def add_milestone():
    try:
        project_id = request.form.get('project_id')
        milestone = ProjectMilestone(
            project_id=project_id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            due_date=datetime.strptime(request.form.get('due_date'), '%Y-%m-%d'),
            payment_amount=float(request.form.get('payment_amount')) if request.form.get('payment_amount') else None
        )
        db.session.add(milestone)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Milestone added successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@admin_bp.route('/milestone/<int:milestone_id>', methods=['POST'])
@login_required
@admin_required
def update_milestone(milestone_id):
    try:
        milestone = ProjectMilestone.query.get_or_404(milestone_id)
        milestone.title = request.form.get('title')
        milestone.description = request.form.get('description')
        milestone.due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')
        milestone.payment_amount = float(request.form.get('payment_amount')) if request.form.get('payment_amount') else None
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Milestone updated successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@admin_bp.route('/milestone/<int:milestone_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_milestone(milestone_id):
    try:
        milestone = ProjectMilestone.query.get_or_404(milestone_id)
        db.session.delete(milestone)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Milestone deleted successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@admin_bp.route('/milestone/<int:milestone_id>/status', methods=['POST'])
@login_required
@admin_required
def update_milestone_status(milestone_id):
    try:
        milestone = ProjectMilestone.query.get_or_404(milestone_id)
        data = request.get_json()
        milestone.status = data.get('status')
        
        if milestone.status == 'completed':
            milestone.completion_date = datetime.utcnow()
            
            # Check if all milestones are completed
            project = milestone.project
            total_milestones = project.milestones.count()
            completed_milestones = project.milestones.filter_by(status='completed').count()
            
            if total_milestones == completed_milestones:
                project.status = 'completed'
                send_project_completed_email(project)
            
            # Send milestone completion notification
            send_milestone_completed_email(milestone)
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'Milestone marked as {milestone.status}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@admin_bp.route('/content')
@login_required
@admin_required
def manage_content():
    team_members = TeamMember.query.order_by(TeamMember.order).all()
    services = Service.query.order_by(Service.order).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).all()
    
    return render_template('admin/content.html',
                         title='Content Management',
                         team_members=team_members,
                         services=services,
                         testimonials=testimonials)

@admin_bp.route('/content/team', methods=['POST'])
@login_required
@admin_required
def update_team():
    name = request.form.get('name')
    role = request.form.get('role')
    bio = request.form.get('bio')
    
    if not all([name, role]):
        flash('Name and role are required.', 'error')
        return redirect(url_for('admin.manage_content'))
    
    member = TeamMember(
        name=name,
        role=role,
        bio=bio,
        order=TeamMember.query.count()
    )
    db.session.add(member)
    db.session.commit()
    
    flash('Team member added successfully!', 'success')
    return redirect(url_for('admin.manage_content'))

@admin_bp.route('/content/service', methods=['POST'])
@login_required
@admin_required
def update_service():
    name = request.form.get('name')
    description = request.form.get('description')
    icon = request.form.get('icon')
    
    if not all([name, description]):
        flash('Name and description are required.', 'error')
        return redirect(url_for('admin.manage_content'))
    
    service = Service(
        name=name,
        description=description,
        icon=icon,
        order=Service.query.count()
    )
    db.session.add(service)
    db.session.commit()
    
    flash('Service added successfully!', 'success')
    return redirect(url_for('admin.manage_content'))

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    # Project statistics
    project_stats = db.session.query(
        Project.status,
        func.count(Project.id)
    ).group_by(Project.status).all()
    
    # Developer statistics
    developer_stats = db.session.query(
        DeveloperProfile.availability_status,
        func.count(DeveloperProfile.id)
    ).group_by(DeveloperProfile.availability_status).all()
    
    # Monthly project creation using SQLite's strftime
    monthly_projects = db.session.query(
        func.strftime('%Y-%m', Project.created_at).label('month'),
        func.count(Project.id).label('count')
    ).group_by(
        func.strftime('%Y-%m', Project.created_at)
    ).order_by(
        func.strftime('%Y-%m', Project.created_at).desc()
    ).all()
    
    # Convert monthly_projects to a list of dictionaries
    monthly_projects_data = [
        {'month': row.month, 'count': row.count}
        for row in monthly_projects
    ]
    
    return render_template('admin/reports.html',
                         title='Reports',
                         project_stats=dict(project_stats),
                         developer_stats=dict(developer_stats),
                         monthly_projects=monthly_projects_data)
