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
```
TheZSolutions/
├── app/
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   │   ├── admin/      # Admin panel templates
│   │   ├── auth/       # Authentication templates
│   │   ├── email/      # Email templates
│   │   └── main/       # Main site templates
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   ├── utils/          # Utility functions
│   └── config.py       # Application configuration
├── logs/               # Application logs
├── migrations/         # Database migrations
├── .env               # Environment variables
└── requirements.txt    # Project dependencies
```

## Features
- User Authentication (Admin, Developer, Customer)
- Project Management
- Developer Portfolio
- Contact Form
- Email Notifications
- File Upload/Download
- Admin Dashboard
- Payment Integration
- Responsive Design

## Checkpoints
1. Initial Setup - Basic project structure and authentication
2. Contact Form - Implemented contact functionality with email notifications
3. Email System - Configured Office 365 SMTP email system with:
   - Custom email templates with embedded logo
   - Base64 image encoding for reliable delivery
   - Professional styling and branding
   - Asynchronous email sending
   - Comprehensive error handling and logging
   - Contact form notifications
   - Project-related notifications

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
