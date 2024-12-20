# TheZSolutions - Professional Software Development Company

## Project Description
TheZSolutions is a professional software development company website built with Flask. It showcases our services, projects, and team while providing functionality for job applications and project requests.

## Requirements
- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Mail
- Tailwind CSS
- Chart.js

## Project Structure
```
TheZSolutions/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # Route handlers
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   └── utils/           # Utility functions
├── migrations/          # Database migrations
├── logs/               # Application logs
├── tests/              # Test files
├── config.py           # Configuration file
├── requirements.txt    # Python dependencies
└── run.py             # Application entry point
```

## Features
1. **Authentication System**
   - User registration and login
   - Role-based access control (Admin, Developer, Customer)
   - Password reset functionality

2. **Admin Dashboard**
   - Project management
   - User management
   - Reports and analytics
   - Job application reviews
   - Project request reviews

3. **Developer Features**
   - Job application system
   - Developer profiles
   - Project assignments

4. **Customer Features**
   - Project request submission
   - Project status tracking
   - Communication system

5. **Public Features**
   - Company services showcase
   - Project portfolio
   - Team member profiles
   - Contact form

## Checkpoints

### Checkpoint 8 (2024-12-20)
- Added job application system for developers
- Added project request system for customers
- Created new database models: JobApplication, ProjectRequest, ProjectRequestAttachment
- Added file upload functionality for resumes and project attachments
- Updated navigation with "Join Us" and "Request Project" links

To restore to this checkpoint:
```bash
git restore --source=checkpoint-8 .
```

### Checkpoint 7 (Previous)
- Fixed reports functionality
- Updated SQLite date formatting
- Fixed JSON serialization issues

To restore to this checkpoint:
```bash
git restore --source=checkpoint-7 .
```

## Installation and Setup
1. Clone the repository:
```bash
git clone https://github.com/engziada/TheZSolutions.git
cd TheZSolutions
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
python run.py
```

## Contributing
1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
- Email: your.email@example.com
- Website: https://www.thezsolutions.com
