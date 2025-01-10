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
def contact():
    form = ContactForm()
    logger = configure_logging()
    
    logger.info("Processing contact form submission")
    logger.debug(f"Form data: {request.form}")
    
    if form.validate_on_submit():
        try:
            # Log form data
            logger.info(f"Form validated successfully")
            logger.info(f"Name: {form.name.data}")
            logger.info(f"Email: {form.email.data}")
            logger.info(f"Subject: {form.subject.data}")
            
            # Create contact record
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            
            logger.info("Saving contact to database")
            db.session.add(contact)
            db.session.commit()
            logger.info(f"Contact saved successfully with ID: {contact.id}")
            
            # Send notification email
            try:
                logger.info("Attempting to send notification email")
                send_contact_notification(contact)
                logger.info("Notification email sent successfully")
                flash(_('Your message has been sent successfully! We will get back to you soon.'), 'success')
            except Exception as e:
                logger.error(f"Failed to send notification email: {str(e)}")
                flash(_('Your message was received but there was an issue sending the notification. Our team will still contact you soon.'), 'warning')
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Database error: {str(e)}")
            flash(_('An error occurred while saving your message. Please try again.'), 'error')
            
    else:
        logger.warning("Form validation failed")
        for field, errors in form.errors.items():
            logger.warning(f"Validation error in {field}: {', '.join(errors)}")
            flash(f"{field}: {', '.join(errors)}", 'error')
    
    return redirect(url_for('main.home', _anchor='contact'))

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
