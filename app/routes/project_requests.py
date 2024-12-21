from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app.models.application import ProjectRequest
from app import db
import os
from datetime import datetime

requests_bp = Blueprint('requests', __name__)

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
                'preferred_contact': request.form.get('preferred_contact'),
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
            
            # Send email notifications (you can implement this later)
            # send_notification_email(project_request)
            
            flash('Your project request has been submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('main.home'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting your project request. Please try again.', 'error')
            current_app.logger.error(f'Error submitting project request: {str(e)}')
            return redirect(url_for('requests.new_request'))
    
    return render_template('requests/new.html', title='Submit Your Project Request')
