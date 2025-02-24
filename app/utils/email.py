from flask import current_app, render_template, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import threading
import base64
import os
from datetime import datetime
from threading import Thread
from flask_mail import Message, Mail
from app import mail
from flask_babel import _

# Configure logging
logger = logging.getLogger('email')
logger.setLevel(logging.INFO)

# Create Log directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Add file handler
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(log_dir, 'email.log'),
    maxBytes=10240,
    backupCount=10,
    delay=True
)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

def get_logo_base64():
    """Get base64 encoded logo for email templates"""
    try:
        logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo.png')
        with open(logo_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{encoded}"
    except Exception as e:
        logger.error(f"Failed to load logo: {str(e)}")
        return None

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            logger.info(f'Email sent successfully to {msg.recipients}')
        except Exception as e:
            logger.error(f'Failed to send email to {msg.recipients}: {str(e)}')
            raise

def send_email(subject, recipients, html_body):
    """Send email using Flask-Mail"""
    try:
        msg = Message(subject=subject, recipients=recipients, html=html_body)
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise

def send_email_async(subject, recipients, html_body):
    """Send email asynchronously using Flask-Mail"""
    try:
        app = current_app._get_current_object()
        msg = Message(subject=subject, recipients=recipients, html=html_body)
        Thread(target=send_async_email, args=(app, msg)).start()
    except Exception as e:
        logger.error(f"Failed to send async email: {str(e)}")
        raise

def render_and_send_email(subject, recipients, template, **kwargs):
    """Render template and send email"""
    try:
        # Render template
        html_content = render_template(f"{template}.html", **kwargs)
        # Send email
        send_email(subject, recipients, html_content)
    except Exception as e:
        logger.error(f"Failed to render and send email: {str(e)}")
        raise

def send_welcome_email(user):
    """Send welcome email to new users"""
    try:
        logger.info(f"Sending welcome email to user: {user.email}")
        render_and_send_email(
            _("Welcome to The Z Solutions"),
            [user.email],
            'email/welcome',
            user=user
        )
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")
        raise

def send_project_created_email(project):
    """Notify developers about new project"""
    try:
        developers = [dev.user.email for dev in project.developers]
        logger.info(f"Sending project created email to developers: {developers}")
        if developers:
            render_and_send_email(
                _("New Project: %(title)s", title=project.title),
                developers,
                'email/project_created',
                project=project
            )
    except Exception as e:
        logger.error(f"Failed to send project created email: {str(e)}")
        raise

def send_project_assigned_email(project, developer):
    """Notify developer about project assignment"""
    try:
        logger.info(f"Sending project assigned email to developer: {developer.user.email}")
        render_and_send_email(
            _("Project Assignment: %(title)s", title=project.title),
            [developer.user.email],
            'email/project_assigned',
            project=project,
            developer=developer
        )
    except Exception as e:
        logger.error(f"Failed to send project assigned email: {str(e)}")
        raise

def send_project_status_update_email(project):
    """Notify stakeholders about project status update"""
    try:
        recipients = [project.customer.email]
        recipients.extend(dev.user.email for dev in project.developers)
        logger.info(f"Sending project status update email to stakeholders: {recipients}")
        render_and_send_email(
            _("Project Status Update: %(title)s", title=project.title),
            recipients,
            'email/project_status_update',
            project=project
        )
    except Exception as e:
        logger.error(f"Failed to send project status update email: {str(e)}")
        raise

def send_milestone_completed_email(milestone):
    """Notify stakeholders about milestone completion"""
    try:
        project = milestone.project
        recipients = [project.customer.email]
        recipients.extend(dev.user.email for dev in project.developers)
        logger.info(f"Sending milestone completed email to stakeholders: {recipients}")
        render_and_send_email(
            _("Milestone Completed: %(title)s", title=milestone.title),
            recipients,
            'email/milestone_completed',
            milestone=milestone,
            project=project
        )
    except Exception as e:
        logger.error(f"Failed to send milestone completed email: {str(e)}")
        raise

def send_payment_received_email(payment):
    """Send payment confirmation to customer and notification to developer"""
    try:
        project = payment.project
        logger.info(f"Sending payment received email to customer: {project.customer.email}")
        
        # Send to customer
        render_and_send_email(
            _("Payment Confirmation"),
            [project.customer.email],
            'email/payment_confirmation',
            payment=payment,
            project=project
        )
        
        # Send to developers
        logger.info(f"Sending payment received email to developers: {[dev.user.email for dev in project.developers]}")
        for developer in project.developers:
            render_and_send_email(
                _("Payment Received"),
                [developer.user.email],
                'email/payment_received',
                payment=payment,
                project=project,
                developer=developer
            )
    except Exception as e:
        logger.error(f"Failed to send payment received email: {str(e)}")
        raise

def send_project_completed_email(project):
    """Notify all stakeholders about project completion"""
    try:
        recipients = [project.customer.email]
        recipients.extend(dev.user.email for dev in project.developers)
        logger.info(f"Sending project completed email to stakeholders: {recipients}")
        render_and_send_email(
            _("Project Completed: %(title)s", title=project.title),
            recipients,
            'email/project_completed',
            project=project
        )
    except Exception as e:
        logger.error(f"Failed to send project completed email: {str(e)}")
        raise

def send_contact_notification(contact):
    """
    Send notification email for new contact form submission
    Args:
        contact: Contact model instance
    """
    try:
        admin_email = current_app.config['ADMIN_EMAIL']
        logger.info(f"Sending contact notification to admin: {admin_email}")
        
        if not admin_email:
            logger.error('No admin email configured for contact notifications')
            return
            
        subject = f'New Contact Form Submission: {contact.subject}'
        logger.info(f"Contact form details - Name: {contact.name}, Email: {contact.email}, Subject: {contact.subject}")
        
        render_and_send_email(
            subject=subject,
            recipients=[admin_email],
            template='email/contact_notification',
            contact=contact
        )
        
    except Exception as e:
        logger.error(f"Failed to send contact notification: {str(e)}")
        raise

def send_application_confirmation(application):
    """
    Send confirmation email to job applicant
    Args:
        application: JobApplication model instance
    """
    try:
        logger.info(f"Sending application confirmation to {application.email}")
        render_and_send_email(
            subject="Application Received",
            recipients=[application.email],
            template="email/application_confirmation",
            first_name=application.first_name,
            last_name=application.last_name,
            position=application.position,
            application_date=application.application_date
        )
    except Exception as e:
        logger.error(f"Failed to send application confirmation: {str(e)}")
        raise

def send_application_notification(application):
    """Send email notifications for new job applications"""
    try:
        current_year = datetime.now().year
        application_date = datetime.now()  # Get current date/time for new applications
        
        # Email to admin
        admin_msg = Message(
            subject=f'New Job Application: {application.first_name} {application.last_name}',
            recipients=[current_app.config['ADMIN_EMAIL']],
            html=render_template('email/application_notification.html',
                first_name=application.first_name,
                last_name=application.last_name,
                email=application.email,
                phone=application.phone,
                position=application.position,
                experience=application.experience,
                skills=application.skills,
                portfolio_url=application.portfolio_url,
                github_url=application.github_url,
                cover_letter=application.cover_letter,
                current_year=current_year,
                application_date=application_date
            )
        )
        
        # Attach resume
        if application.resume_path:
            with open(os.path.join(current_app.config['RESUMES_FOLDER'], application.resume_path), 'rb') as f:
                admin_msg.attach(
                    application.resume_path,
                    'application/pdf' if application.resume_path.endswith('.pdf') else 'application/msword',
                    f.read()
                )
        
        mail.send(admin_msg)
        
        # Confirmation email to applicant
        applicant_msg = Message(
            subject='Application Received - The Z Solutions',
            recipients=[application.email],
            html=render_template('email/application_confirmation.html',
                first_name=application.first_name,
                position=application.position,
                current_year=current_year,
                application_date=application_date
            )
        )
        mail.send(applicant_msg)
        
        return True
    except Exception as e:
        current_app.logger.error(f'Error sending application emails: {str(e)}')
        return False

def send_project_request_confirmation(project_request):
    """
    Send confirmation email to project requester
    Args:
        project_request: ProjectRequest model instance
    """
    try:
        logger.info(f"Sending project request confirmation to {project_request.contact_email}")
        render_and_send_email(
            subject="Project Request Received",
            recipients=[project_request.contact_email],
            template="email/project_request_confirmation",
            **project_request.__dict__
        )
    except Exception as e:
        logger.error(f"Failed to send project request confirmation: {str(e)}")
        raise

def send_project_request_notification(project_request):
    """Send email notifications for new project requests"""
    try:
        current_year = datetime.now().year
        
        # Format budget range
        budget_range = f"${project_request.budget_min:,.2f}"
        if project_request.budget_max and project_request.budget_max != project_request.budget_min:
            budget_range += f" - ${project_request.budget_max:,.2f}"
        
        # Confirmation email to requester first
        html = render_template('email/project_request_confirmation.html',
            contact_name=project_request.contact_name,
            project_name=project_request.title,  
            current_year=current_year
        )
        send_email(
            subject='Project Request Received - The Z Solutions',
            recipients=[project_request.contact_email],
            html_body=html
        )
        
        # Then email to admin
        admin_html = render_template('email/project_request_notification.html',
            project_name=project_request.title,  
            project_type=project_request.category,  
            description=project_request.description,
            features=project_request.features,
            timeline=project_request.timeline,
            budget_range=budget_range,  
            contact_name=project_request.contact_name,
            contact_email=project_request.contact_email,
            contact_phone=project_request.contact_phone,
            preferred_contact=project_request.preferred_contact,
            created_at=project_request.created_at,
            files=project_request.files,
            current_year=current_year
        )
        
        msg = Message(
            subject=f'New Project Request: {project_request.title}',  
            recipients=[current_app.config['ADMIN_EMAIL']],
            html=admin_html
        )
        
        # Attach project files
        if project_request.files:
            for file in project_request.files:
                with open(os.path.join(current_app.config['PROJECT_FILES_FOLDER'], file.filename), 'rb') as f:
                    msg.attach(
                        file.filename,
                        'application/pdf' if file.filename.endswith('.pdf') else 'application/octet-stream',
                        f.read()
                    )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        current_app.logger.error(f'Error sending project request emails: {str(e)}')
        return False

def send_project_request_rejection(project_request):
    """Send rejection email for project request"""
    subject = _("Update Regarding Your Project Request")
    
    html = render_template('email/project_request_rejection.html',
                         contact_name=project_request.contact_name,
                         project_name=project_request.project_name)
    
    send_email(subject=subject,
              recipients=[project_request.contact_email],
              html_body=html)

def send_project_request_approval(project_request):
    """Send approval email for project request"""
    subject = _("Your Project Request Has Been Approved!")
    
    html = render_template('email/project_request_approval.html',
                         contact_name=project_request.contact_name,
                         project_name=project_request.project_name)
    
    send_email(subject=subject,
              recipients=[project_request.contact_email],
              html_body=html)

def send_application_rejection(application):
    """Send rejection email to job applicant"""
    try:
        html = render_template('email/application_rejection.html',
                           application=application)
        send_email(
            subject=_("Update on Your Application - The Z Solutions"),
            recipients=[application.email],
            html_body=html
        )
        current_app.logger.info(f'Rejection email sent to {application.email}')
    except Exception as e:
        current_app.logger.error(f'Failed to send rejection email to {application.email}: {str(e)}')
        raise

def send_application_shortlisted(application):
    """Send shortlist notification email to job applicant"""
    try:
        html = render_template('email/application_shortlisted.html',
                           application=application)
        send_email(
            subject=_("Your Application Has Been Shortlisted - The Z Solutions"),
            recipients=[application.email],
            html_body=html
        )
        current_app.logger.info(f'Shortlist notification email sent to {application.email}')
    except Exception as e:
        current_app.logger.error(f'Failed to send shortlist notification email to {application.email}: {str(e)}')
        raise

def test_smtp_connection():
    """Test SMTP connection and authentication"""
    try:
        # Get configuration
        smtp_server = current_app.config['MAIL_SERVER']
        smtp_port = current_app.config['MAIL_PORT']
        username = current_app.config['MAIL_USERNAME']
        password = current_app.config['MAIL_PASSWORD']
        
        logger.info(f"Testing SMTP connection to {smtp_server}:{smtp_port}")
        logger.info(f"Using username: {username}")
        
        # Try to connect
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            logger.info("Successfully connected to SMTP server")
            
            # Start TLS
            server.starttls()
            logger.info("TLS connection established")
            
            # Try to login
            server.login(username, password)
            logger.info("Successfully authenticated with SMTP server")
            
            return True, "SMTP connection test successful"
            
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Authentication failed: {str(e)}")
        return False, f"Authentication failed: {str(e)}"
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {str(e)}")
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        return False, f"Connection test failed: {str(e)}"
