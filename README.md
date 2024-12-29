# The Z Solutions

A professional software development services platform built with Flask.

## Project Description
The Z Solutions is a comprehensive platform for managing software development projects, connecting clients with skilled developers, and facilitating project collaboration.

## Requirements
- Python 3.11+
- Flask
- SQLAlchemy
- Flask-Mail
- Other dependencies in requirements.txt

## Project Structure
- `app/`: Main application directory
  - `models/`: Database models
    - `application.py`: Models for job applications and project requests
    - `project.py`: Models for projects and related entities
  - `routes/`: Route handlers
    - `project_requests.py`: Handles project request submissions
  - `templates/`: HTML templates
    - `components/`: Reusable UI components
      - `loading_overlay.html`: Matrix-style loading animation with logo
    - `careers/`: Career-related templates
      - `apply.html`: Job application form
    - `requests/`: Project request templates
      - `new.html`: Project request form
    - `email/`: Email templates
      - `project_request_confirmation.html`: Email sent to requester
      - `project_request_notification.html`: Email sent to admin
  - `static/`: Static files
    - `img/`: Images including logo
  - `utils/`: Utility functions
    - `email.py`: Email sending functions
  - `config.py`: Application configuration
- `logs/`: Application logs
- `migrations/`: Database migrations
- `.env`: Environment variables
- `requirements.txt`: Project dependencies

## Features
1. Project Request System
   - Form submission with file uploads
   - Email notifications (requester & admin)
   - File storage with database tracking
   - Form validation and security

2. Job Application System
   - Application form with resume upload
   - Email notifications
   - Application tracking

3. UI Components
   - Matrix-style loading overlay
     - Falling 0's, 1's, and Z's animation
     - Fading logo effect
     - Reusable component

## Checkpoints
### Checkpoint 2 (2024-12-29)
- Added ProjectRequestFile model for handling file uploads
- Created reusable loading overlay component
- Enhanced form submission UX with:
  - Matrix-style loading animation
  - Fading logo effect
  - Submit button disabling
  - File upload progress feedback
- Fixed project request file handling
- Improved email notifications with file attachments
- Added database migrations for new models

### Checkpoint 1 (Previous)
- Initial project setup
- Basic form implementations
- Email notification system
- Database models and migrations

## Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure environment variables
6. Run migrations: `flask db upgrade`
7. Start the server: `python run.py`

## Environment Variables
Required environment variables in `.env`:
```
# Email Configuration
MAIL_USERNAME=your_email@domain.com
MAIL_PASSWORD='your_password'

# Application Security
SECRET_KEY='your_secret_key'
