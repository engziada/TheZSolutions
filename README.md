# Z Solutions Website

A professional software development company website built with Flask.

## Project Description
Z Solutions website showcases our software development services, team, and portfolio. Built with Python Flask for robust backend functionality and modern frontend technologies for a seamless user experience.

## Requirements
- Python 3.8+
- Flask
- SQLAlchemy
- Other dependencies in requirements.txt

## Project Structure
```
TheZSolutions/
├── app/
│   ├── static/          # Static files (CSS, JS, images)
│   ├── templates/       # HTML templates
│   ├── routes/          # Route handlers
│   ├── models/          # Database models
│   └── utils/           # Utility functions
├── logs/                # Application logs
├── migrations/          # Database migrations
└── tests/              # Test files
```

## Features
1. **User Management**
   - Authentication system
   - User roles (Admin, Developer, Customer)
   - Profile management

2. **Project Management**
   - Project showcase
   - Project requests
   - Project status tracking

3. **Career Portal**
   - Job listings
   - Application system
   - Team showcase

4. **Content Management**
   - Dynamic content updates
   - SEO optimization
   - Image optimization

5. **SEO Optimization**
   - Meta tags optimization
   - Open Graph integration
   - Dynamic sitemap generation
   - Robots.txt configuration

## Translations

The project uses Flask-Babel for internationalization (i18n) and localization (l10n). Here's how the translation system works:

### Translation Files
- `messages.pot`: Template file containing all translatable strings
- `app/translations/ar/LC_MESSAGES/messages.po`: Arabic translations
- `app/translations/ar/LC_MESSAGES/messages.mo`: Compiled Arabic translations

### Translation Workflow
1. Extract strings to messages.pot:
```bash
pybabel extract -F babel.cfg -o messages.pot .
```

2. Create/Update translation files:
```bash
# First time (init):
pybabel init -i messages.pot -d app/translations -l ar

# Update existing translations:
pybabel update -i messages.pot -d app/translations
```

3. Edit translations in `app/translations/ar/LC_MESSAGES/messages.po`

4. Compile translations:
```bash
pybabel compile -d app/translations
```

### Adding a New Language
1. Initialize the language (e.g., for French):
```bash
pybabel init -i messages.pot -d app/translations -l fr
```

2. Edit the new translation file in `app/translations/fr/LC_MESSAGES/messages.po`

3. Compile translations as shown above

## Checkpoints

### Checkpoint 1 (2024-01-03)
- Initial project setup
- Basic structure implementation
- Authentication system
```bash
git checkout tags/checkpoint-1
```

### Checkpoint 2 (2024-01-03)
- Hero section implementation
- Image optimization
- Loading performance improvements
```bash
git checkout tags/checkpoint-2
```

### Checkpoint 3 (2024-01-03)
- SEO Optimization
  - Enhanced meta tags
  - Open Graph implementation
  - Dynamic sitemap generation
  - Robots.txt configuration
  - Social media preview optimization
```bash
git checkout tags/checkpoint-3
```

### Checkpoint 6 - Translation System Complete (2025-01-10 01:19:24+02:00)

### Changes Made
1. **Developer Routes**
   - Added translation markers for all access control messages
   - Added translation markers for project status updates
   - Added translation markers for application and profile messages

2. **Customer Routes**
   - Added translation markers for access control messages
   - Added translation markers for project-related messages
   - Added translation markers for file upload messages

3. **Email System**
   - Added translation markers for all email subjects
   - Added translations for project notifications
   - Added translations for payment notifications
   - Added translations for application status updates

4. **Arabic Translations**
   - Added new Arabic translations for all messages
   - Ensured proper formatting for messages with variables
   - Compiled translations to .mo file

### Files Modified
- `app/routes/developer.py`: Added translation markers and imported Flask-Babel
- `app/routes/customer.py`: Added translation markers and imported Flask-Babel
- `app/utils/email.py`: Added translation markers for email subjects
- `app/translations/ar/LC_MESSAGES/messages.po`: Added new Arabic translations
- `app/translations/ar/LC_MESSAGES/messages.mo`: Compiled translation file

### Command to Revert to This Checkpoint
```bash
git checkout $(git rev-list -n 1 --before="2025-01-10 01:19:24" main)
```

### Checkpoint 1
- Date: 2025-01-10 15:26:16
- Description: Updated mobile navbar to include language switcher with icons and improved styling.

## Getting Started
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run migrations: `flask db upgrade`
5. Start the server: `flask run`

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
