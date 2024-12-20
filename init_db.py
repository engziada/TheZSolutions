from app import create_app, db
from app.models.project import Project, ProjectRequirement, ProjectMilestone, ProjectFile

app = create_app()

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()
        
        # Add some sample projects if the table is empty
        if not Project.query.first():
            # Web Project
            web_project = Project(
                title="E-Commerce Platform",
                description="A modern e-commerce platform built with Flask and React",
                category="web",
                status="completed",
                budget_min=15000,
                budget_max=25000,
                customer_id=1  # Make sure this ID exists
            )
            
            # Desktop Project
            desktop_project = Project(
                title="Inventory Management System",
                description="A desktop application for managing inventory and sales",
                category="desktop",
                status="completed",
                budget_min=10000,
                budget_max=20000,
                customer_id=1  # Make sure this ID exists
            )
            
            # Mobile Project
            mobile_project = Project(
                title="Fitness Tracking App",
                description="A mobile app for tracking workouts and nutrition",
                category="mobile",
                status="completed",
                budget_min=12000,
                budget_max=18000,
                customer_id=1  # Make sure this ID exists
            )
            
            # Add projects to session
            db.session.add(web_project)
            db.session.add(desktop_project)
            db.session.add(mobile_project)
            
            # Commit the session
            db.session.commit()
            
            print("Database initialized with sample projects!")
        else:
            print("Database already contains projects.")

if __name__ == '__main__':
    init_db()
