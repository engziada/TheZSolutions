from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, template, **kwargs):
    """
    Send email using a template
    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        template: Template name without extension (e.g., 'email/welcome')
        **kwargs: Variables to pass to the template
    """
    app = current_app._get_current_object()
    msg = Message(
        subject=f"The Z Solutions - {subject}",
        recipients=recipients,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    msg.html = render_template(f"{template}.html", **kwargs)
    
    # Send email asynchronously
    Thread(target=send_async_email, args=(app, msg)).start()

def send_welcome_email(user):
    """Send welcome email to new users"""
    send_email(
        "Welcome to The Z Solutions",
        [user.email],
        'email/welcome',
        user=user
    )

def send_project_created_email(project):
    """Notify developers about new project"""
    developers = [dev.user.email for dev in project.developers]
    if developers:
        send_email(
            f"New Project: {project.title}",
            developers,
            'email/project_created',
            project=project
        )

def send_project_assigned_email(project, developer):
    """Notify developer about project assignment"""
    send_email(
        f"Project Assignment: {project.title}",
        [developer.user.email],
        'email/project_assigned',
        project=project,
        developer=developer
    )

def send_project_status_update_email(project):
    """Notify stakeholders about project status update"""
    recipients = [project.customer.email]
    recipients.extend(dev.user.email for dev in project.developers)
    
    send_email(
        f"Project Status Update: {project.title}",
        recipients,
        'email/project_status_update',
        project=project
    )

def send_milestone_completed_email(milestone):
    """Notify stakeholders about milestone completion"""
    project = milestone.project
    recipients = [project.customer.email]
    recipients.extend(dev.user.email for dev in project.developers)
    
    send_email(
        f"Milestone Completed: {milestone.title}",
        recipients,
        'email/milestone_completed',
        milestone=milestone,
        project=project
    )

def send_payment_received_email(payment):
    """Send payment confirmation to customer and notification to developer"""
    project = payment.project
    
    # Notify customer
    send_email(
        "Payment Confirmation",
        [project.customer.email],
        'email/payment_confirmation',
        payment=payment,
        project=project
    )
    
    # Notify developers
    for developer in project.developers:
        send_email(
            "Payment Received",
            [developer.user.email],
            'email/payment_received',
            payment=payment,
            project=project,
            developer=developer
        )

def send_project_completed_email(project):
    """Notify all stakeholders about project completion"""
    recipients = [project.customer.email]
    recipients.extend(dev.user.email for dev in project.developers)
    
    send_email(
        f"Project Completed: {project.title}",
        recipients,
        'email/project_completed',
        project=project
    )

def send_contact_notification(contact):
    """
    Send notification email for new contact form submission
    Args:
        contact: Contact model instance
    """
    admin_email = current_app.config['ADMIN_EMAIL']
    if not admin_email:
        current_app.logger.warning('No admin email configured for contact notifications')
        return
        
    subject = f'New Contact Form Submission: {contact.subject}'
    
    send_email(
        subject=subject,
        recipients=[admin_email],
        template='email/contact_notification',
        contact=contact
    )
