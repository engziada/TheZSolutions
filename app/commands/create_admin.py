from flask.cli import with_appcontext
import click
from app import db
from app.models.user import User

@click.command('create-admin')
@click.option('--email', prompt='Admin email', help='Email address for the admin user')
@click.option('--username', prompt='Admin username', help='Username for the admin user')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password for the admin user')
@with_appcontext
def create_admin_command(email, username, password):
    """Create an admin user."""
    try:
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            click.echo('Error: A user with that email already exists.')
            return
        
        if User.query.filter_by(username=username).first():
            click.echo('Error: A user with that username already exists.')
            return
        
        # Create new admin user
        user = User(email=email, username=username, role='admin')
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        click.echo(f'Successfully created admin user: {username}')
        
    except Exception as e:
        click.echo(f'Error creating admin user: {str(e)}')
        db.session.rollback() 