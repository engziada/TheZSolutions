from flask import current_app, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import threading
import base64
import os

logger = logging.getLogger(__name__)

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

def send_email_direct(subject, recipients, html_content):
    """Send email directly using smtplib"""
    try:
        # Get configuration
        smtp_server = current_app.config['MAIL_SERVER']
        smtp_port = current_app.config['MAIL_PORT']
        username = current_app.config['MAIL_USERNAME']
        password = current_app.config['MAIL_PASSWORD']
        sender = current_app.config['MAIL_DEFAULT_SENDER'][1]  # Get email from tuple
        
        logger.info(f"Attempting to connect to SMTP server: {smtp_server}:{smtp_port}")
        logger.debug(f"Using username: {username}")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"The Z Solutions - {subject}"
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        
        # Attach HTML content
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            logger.info("Connected to SMTP server")
            
            # Start TLS
            server.starttls()
            logger.info("TLS started")
            
            # Login
            logger.info(f"Attempting to login as {username}")
            server.login(username, password)
            logger.info("Login successful")
            
            # Send email
            logger.info(f"Sending email to {recipients}")
            server.send_message(msg)
            logger.info("Email sent successfully")
            
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise

def send_email_async(subject, recipients, template, **kwargs):
    """Send email asynchronously"""
    try:
        app = current_app._get_current_object()
        def _send():
            with app.app_context():
                # Render template
                html_content = render_template(f"{template}.html", **kwargs)
                # Send email
                send_email_direct(subject, recipients, html_content)
        
        thread = threading.Thread(target=_send)
        thread.start()
        
    except Exception as e:
        logger.error(f"Failed to send async email: {str(e)}")
        raise

def send_email(subject, recipients, template, **kwargs):
    """
    Send email using a template
    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        template: Template name without extension (e.g., 'email/welcome')
        **kwargs: Variables to pass to the template
    """
    try:
        logger.info(f"Preparing email with subject '{subject}' for recipients: {recipients}")
        
        # Add logo to template variables
        kwargs['logo_base64'] = get_logo_base64()
        
        # Render template
        html_content = render_template(f"{template}.html", **kwargs)
        
        # Send email
        send_email_direct(subject, recipients, html_content)
        
    except Exception as e:
        logger.error(f"Error preparing email: {str(e)}")
        raise

def send_welcome_email(user):
    """Send welcome email to new users"""
    try:
        logger.info(f"Sending welcome email to user: {user.email}")
        send_email_async(
            "Welcome to The Z Solutions",
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
            send_email_async(
                f"New Project: {project.title}",
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
        send_email_async(
            f"Project Assignment: {project.title}",
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
        send_email_async(
            f"Project Status Update: {project.title}",
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
        send_email_async(
            f"Milestone Completed: {milestone.title}",
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
        send_email_async(
            "Payment Confirmation",
            [project.customer.email],
            'email/payment_confirmation',
            payment=payment,
            project=project
        )
        
        # Send to developers
        logger.info(f"Sending payment received email to developers: {[dev.user.email for dev in project.developers]}")
        for developer in project.developers:
            send_email_async(
                "Payment Received",
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
        send_email_async(
            f"Project Completed: {project.title}",
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
        
        send_email(
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
        send_email(
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
    """
    Send notification email to admin about new job application
    Args:
        application: JobApplication model instance
    """
    try:
        admin_email = current_app.config['ADMIN_EMAIL']
        logger.info(f"Sending application notification to admin: {admin_email}")
        send_email(
            subject=f"New Job Application - {application.position}",
            recipients=[admin_email],
            template="email/application_notification",
            **application.__dict__
        )
    except Exception as e:
        logger.error(f"Failed to send application notification: {str(e)}")
        raise

def send_project_request_confirmation(project_request):
    """
    Send confirmation email to project requester
    Args:
        project_request: ProjectRequest model instance
    """
    try:
        logger.info(f"Sending project request confirmation to {project_request.contact_email}")
        send_email(
            subject="Project Request Received",
            recipients=[project_request.contact_email],
            template="email/project_request_confirmation",
            **project_request.__dict__
        )
    except Exception as e:
        logger.error(f"Failed to send project request confirmation: {str(e)}")
        raise

def send_project_request_notification(project_request, files=None):
    """
    Send notification email to admin about new project request
    Args:
        project_request: ProjectRequest model instance
        files: List of uploaded files (optional)
    """
    try:
        admin_email = current_app.config['ADMIN_EMAIL']
        logger.info(f"Sending project request notification to admin: {admin_email}")
        
        # Prepare template data
        template_data = project_request.__dict__
        if files:
            template_data['files'] = files
            
        send_email(
            subject=f"New Project Request - {project_request.project_name}",
            recipients=[admin_email],
            template="email/project_request_notification",
            **template_data
        )
    except Exception as e:
        logger.error(f"Failed to send project request notification: {str(e)}")
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
