from app import create_app, db
from app.models.user import User, DeveloperProfile

app = create_app()

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@thezolutions.com').first()
        if not admin:
            # Create admin user
            admin = User(
                email='admin@thezolutions.com',
                username='admin',
                role='admin'
            )
            admin.set_password('Admin@123')  # Set a secure default password
            
            # Create developer profile for admin
            dev_profile = DeveloperProfile(
                user=admin,
                skills=['Python', 'Flask', 'JavaScript', 'React', 'SQL'],
                experience_years=10,
                portfolio_url='https://thezolutions.com/portfolio',
                github_url='https://github.com/muhammadz',
                linkedin_url='https://linkedin.com/in/muhammadz',
                bio='Experienced software developer and team leader with a passion for creating innovative solutions.',
                hourly_rate=100.0,
                availability_status='available'
            )
            
            # Add to database
            db.session.add(admin)
            db.session.add(dev_profile)
            db.session.commit()
            
            print("Admin user created successfully!")
            print("Email: admin@thezolutions.com")
            print("Password: Admin@123")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_admin()
