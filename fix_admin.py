from app import create_app, db
from app.models.user import User, DeveloperProfile

app = create_app()

def fix_admin():
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(email='admin@thezolutions.com').first()
        
        if admin:
            print(f"Found admin user: {admin.username}")
            print(f"Current role: {admin.role}")
            
            # Fix admin role if needed
            if admin.role != 'admin':
                print("Fixing admin role...")
                admin.role = 'admin'
                db.session.commit()
                print("Admin role fixed!")
            else:
                print("Admin role is correct!")
            
            # Check if developer profile exists
            if not admin.developer_profile:
                print("Creating developer profile for admin...")
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
                db.session.add(dev_profile)
                db.session.commit()
                print("Developer profile created!")
            else:
                print("Developer profile exists!")
        else:
            print("Admin user not found! Creating new admin user...")
            admin = User(
                email='admin@thezolutions.com',
                username='admin',
                role='admin'
            )
            admin.set_password('Admin@123')
            
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
            
            db.session.add(admin)
            db.session.add(dev_profile)
            db.session.commit()
            print("Admin user created successfully!")
            print("Email: admin@thezolutions.com")
            print("Password: Admin@123")

if __name__ == '__main__':
    fix_admin()
