from flask import Blueprint, render_template, jsonify, request, abort, redirect, url_for, flash, current_app, session
from flask_login import current_user
from app.forms.contact import ContactForm
from app.utils.email import send_contact_notification, test_smtp_connection
from app.models.contact import Contact
from app.models.project import Project
from app import db
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_babel import _
from app import limiter
from flask_limiter.util import get_remote_address
import re
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

# Configure logging
def configure_logging():
    log_file = os.path.join(current_app.config['LOG_FOLDER'], 'contact.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    logger = logging.getLogger('contact')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    return logger

@main_bp.route('/')
@main_bp.route('/home')
def home():
    form = ContactForm()
    return render_template('main/home.html', title='Home', form=form)

@main_bp.route('/services')
def services():
    return render_template('main/services.html', title='Our Services')

@main_bp.route('/projects')
def projects():
    # Get recent completed projects
    recent_projects = Project.query.filter_by(status='completed')\
        .order_by(Project.end_date.desc())\
        .limit(6)\
        .all()
    
    # Get projects by category
    web_projects = Project.query.filter_by(category='web', status='completed').limit(3).all()
    desktop_projects = Project.query.filter_by(category='desktop', status='completed').limit(3).all()
    mobile_projects = Project.query.filter_by(category='mobile', status='completed').limit(3).all()
    
    return render_template('main/projects.html',
                         title='Recent Projects',
                         recent_projects=recent_projects,
                         web_projects=web_projects,
                         desktop_projects=desktop_projects,
                         mobile_projects=mobile_projects)

@main_bp.route('/team')
def team():
    return render_template('main/team.html', title='Our Team')

@main_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('main/project_detail.html',
                         title=project.title,
                         project=project)

@main_bp.route('/portfolio')
def portfolio():
    # Ensure the language is set based on the session variable
    current_language = session.get('language', 'en')  # Default to English if not set
    return render_template('main/portfolio.html', title='Portfolio', language=current_language)

@main_bp.route('/contact', methods=['GET'])
def contact_page():
    form = ContactForm()
    return render_template('main/contact.html', title='Contact Us', form=form)

@main_bp.route('/contact', methods=['POST'])
@limiter.limit("1 per hour", key_func=get_remote_address)
def contact():
    form = ContactForm()
    logger = configure_logging()
    
    # If the request is AJAX/Fetch
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            if not form.validate_on_submit():
                return jsonify({'status': 'error', 'message': _('Invalid form data')}), 400
                
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data,
                ip_address=request.remote_addr
            )
            db.session.add(contact)
            db.session.commit()
            
            send_contact_notification(contact)
            return jsonify({
                'status': 'success',
                'message': _('Your message has been sent! We will get back to you soon.')
            })
            
        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}")
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': _('An error occurred. Please try again later.')
            }), 500
    
    # If the request is regular form submission
    try:
        if form.validate_on_submit():
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data,
                ip_address=request.remote_addr
            )
            db.session.add(contact)
            db.session.commit()
            
            send_contact_notification(contact)
            flash(_('Your message has been sent! We will get back to you soon.'), 'success')
            return redirect(url_for('main.home'))
            
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        db.session.rollback()
        flash(_('An error occurred. Please try again later.'), 'error')
            
    return render_template('main/home.html', form=form)

@main_bp.route('/test_email')
def test_email():
    """Test email configuration"""
    from app.utils.email import test_smtp_connection
    
    success, message = test_smtp_connection()
    if success:
        flash(_('Email configuration test successful!'), 'success')
    else:
        flash(_('Email configuration test failed: %s') % message, 'error')
    
    return redirect(url_for('main.home'))

@main_bp.route('/language/<lang>')
def set_language(lang):
    if lang in ['en', 'ar']:
        session['language'] = lang
    return redirect(request.referrer or url_for('main.index'))





