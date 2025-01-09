from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models.user import DeveloperProfile
from app.models.project import Project
from app import db
from datetime import datetime
import json
from flask_babel import _

developer_bp = Blueprint('developer', __name__)

@developer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'developer':
        flash(_('Access denied. Developer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    # Get developer's active projects and available projects
    active_projects = Project.query.join(
        Project.developers
    ).filter(
        DeveloperProfile.user_id == current_user.id
    ).all()
    
    available_projects = Project.query.filter(
        Project.status == 'pending'
    ).all()
    
    return render_template('developer/dashboard.html',
                         title='Developer Dashboard',
                         active_projects=active_projects,
                         available_projects=available_projects)

@developer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'developer':
        flash(_('Access denied. Developer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    profile = current_user.developer_profile
    
    if request.method == 'POST':
        # Update skills - convert list to JSON
        skills = request.form.getlist('skills[]')
        profile.skills = json.dumps(skills)
        
        # Update other profile information
        profile.experience_years = int(request.form.get('experience_years', 0))
        profile.portfolio_url = request.form.get('portfolio_url')
        profile.github_url = request.form.get('github_url')
        profile.linkedin_url = request.form.get('linkedin_url')
        profile.bio = request.form.get('bio')
        profile.hourly_rate = float(request.form.get('hourly_rate', 0))
        profile.availability_status = request.form.get('availability_status')
        
        db.session.commit()
        flash(_('Profile updated successfully!'), 'success')
        return redirect(url_for('developer.profile'))
    
    return render_template('developer/profile.html',
                         title='Developer Profile',
                         profile=profile)

@developer_bp.route('/project/<int:project_id>')
@login_required
def view_project(project_id):
    if current_user.role != 'developer':
        flash(_('Access denied. Developer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    project = Project.query.get_or_404(project_id)
    
    # Check if developer is assigned to this project
    if project.status != 'pending' and current_user.developer_profile not in project.developers:
        flash(_('Access denied. You are not assigned to this project.'), 'error')
        return redirect(url_for('developer.dashboard'))
    
    return render_template('developer/view_project.html',
                         title=f'Project: {project.title}',
                         project=project)

@developer_bp.route('/project/<int:project_id>/apply', methods=['POST'])
@login_required
def apply_project(project_id):
    if current_user.role != 'developer':
        flash(_('Access denied. Developer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    project = Project.query.get_or_404(project_id)
    
    if project.status != 'pending':
        flash(_('This project is no longer accepting applications.'), 'error')
        return redirect(url_for('developer.dashboard'))
    
    if current_user.developer_profile in project.developers:
        flash(_('You have already applied to this project.'), 'info')
    else:
        project.developers.append(current_user.developer_profile)
        db.session.commit()
        flash(_('Application submitted successfully!'), 'success')
    
    return redirect(url_for('developer.view_project', project_id=project.id))

@developer_bp.route('/project/<int:project_id>/update-status', methods=['POST'])
@login_required
def update_project_status(project_id):
    if current_user.role != 'developer':
        flash(_('Access denied. Developer access only.'), 'error')
        return redirect(url_for('main.home'))
    
    project = Project.query.get_or_404(project_id)
    
    if current_user.developer_profile not in project.developers:
        flash(_('Access denied. You are not assigned to this project.'), 'error')
        return redirect(url_for('developer.dashboard'))
    
    status = request.form.get('status')
    if status in ['in_progress', 'completed']:
        project.status = status
        db.session.commit()
        flash(_('Project status updated to %(status)s.', status=status), 'success')
    
    return redirect(url_for('developer.view_project', project_id=project.id))
