from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import current_user
from app.forms.contact import ContactForm
from app.utils.email import send_contact_notification
from app.models.contact import Contact
from app.models.project import Project
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    return render_template('main/home.html', title='Home')

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

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Create contact record
                contact = Contact(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    phone=form.phone.data,
                    subject=form.subject.data,
                    message=form.message.data
                )
                db.session.add(contact)
                db.session.commit()
                
                # Send notification email
                send_contact_notification(contact)
                
                return jsonify({
                    'status': 'success',
                    'message': 'Your message has been sent successfully!'
                })
                
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'status': 'error',
                    'message': 'An error occurred. Please try again.'
                }), 500
        
        return jsonify({
            'status': 'error',
            'message': 'Please check your input and try again.',
            'errors': form.errors
        }), 400
    
    return render_template('main/contact.html', title='Contact Us', form=form)
