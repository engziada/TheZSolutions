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
