from flask import Blueprint, Response, url_for, request, current_app
from app.models.project import Project
from datetime import datetime
from app import db
import logging

seo_bp = Blueprint('seo', __name__)
logger = logging.getLogger(__name__)

@seo_bp.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml dynamically."""
    try:
        pages = []
        ten_days_ago = datetime.now().strftime('%Y-%m-%d')
        
        # Add static pages with their priorities
        static_pages = {
            'main.home': {'priority': '1.0', 'changefreq': 'daily'},
            'main.about': {'priority': '0.8', 'changefreq': 'weekly'},
            'main.contact': {'priority': '0.8', 'changefreq': 'weekly'},
            'projects.list_projects': {'priority': '0.9', 'changefreq': 'daily'},
            'careers.list_positions': {'priority': '0.9', 'changefreq': 'daily'},
        }
        
        # Add static pages
        for rule, options in static_pages.items():
            pages.append({
                'loc': url_for(rule, _external=True),
                'lastmod': ten_days_ago,
                'changefreq': options['changefreq'],
                'priority': options['priority']
            })
        
        # Add dynamic project pages
        projects = Project.query.all()
        for project in projects:
            pages.append({
                'loc': url_for('projects.view_project', project_id=project.id, _external=True),
                'lastmod': project.updated_at.strftime('%Y-%m-%d'),
                'changefreq': 'weekly',
                'priority': '0.7'
            })
        
        # Generate sitemap XML
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        sitemap_xml += 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        sitemap_xml += 'xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 '
        sitemap_xml += 'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n'
        
        for page in pages:
            sitemap_xml += '  <url>\n'
            sitemap_xml += f'    <loc>{page["loc"]}</loc>\n'
            sitemap_xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
            sitemap_xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
            sitemap_xml += f'    <priority>{page["priority"]}</priority>\n'
            sitemap_xml += '  </url>\n'
        
        sitemap_xml += '</urlset>'
        
        logger.info(f'Sitemap generated successfully with {len(pages)} URLs')
        return Response(sitemap_xml, mimetype='application/xml')
    
    except Exception as e:
        logger.error(f'Error generating sitemap: {str(e)}')
        return Response('Error generating sitemap', status=500)

@seo_bp.route('/robots.txt')
def robots():
    """Serve robots.txt dynamically."""
    try:
        domain = request.host_url.rstrip('/')
        robots_txt = f"""User-agent: *
Allow: /

# Dynamic sitemap
Sitemap: {domain}/sitemap.xml

# Protected routes
Disallow: /admin/*
Disallow: /login
Disallow: /register
Disallow: /reset-password
Disallow: /uploads/*
"""
        logger.info('Robots.txt served successfully')
        return Response(robots_txt, mimetype='text/plain')
    
    except Exception as e:
        logger.error(f'Error serving robots.txt: {str(e)}')
        return Response('Error serving robots.txt', status=500)
