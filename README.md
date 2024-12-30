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
1. Initial project setup with basic structure and dependencies (December 28, 2024, 23:45:12)
2. Added user authentication and basic templates (December 29, 2024, 00:30:45)
3. Added project request and job application features (December 29, 2024, 02:11:55)
4. Added project request file handling and reusable loading overlay (December 29, 2024, 23:20:54)
5. Unified notification system across all forms (December 30, 2024, 14:27:28)
   - Contact form now uses the same loading overlay and notification system as project requests
   - Improved form submission UX with disabled buttons during submission
   - Consistent notification style across all forms

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
