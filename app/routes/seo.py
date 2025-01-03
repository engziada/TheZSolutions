from flask import Blueprint, Response, url_for, request, current_app
from app.models.project import Project
from datetime import datetime
from app import db
import logging

# Create blueprint with explicit url_prefix
seo_bp = Blueprint('seo', __name__, url_prefix='')

# Configure logging
logger = logging.getLogger(__name__)

@seo_bp.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml dynamically."""
    try:
        pages = []
        ten_days_ago = datetime.now().strftime('%Y-%m-%d')
        
        # Add static pages with their priorities
        static_pages = [
            {'route': 'main.home', 'priority': '1.0', 'changefreq': 'daily'},
            {'route': 'main.services', 'priority': '0.9', 'changefreq': 'weekly'},
            {'route': 'main.contact_page', 'priority': '0.8', 'changefreq': 'weekly'},
            {'route': 'main.projects', 'priority': '0.9', 'changefreq': 'daily'},
            {'route': 'main.portfolio', 'priority': '0.9', 'changefreq': 'daily'}
        ]
        
        # Add static pages
        for page in static_pages:
            try:
                url = url_for(page['route'], _external=True)
                pages.append({
                    'loc': url,
                    'lastmod': ten_days_ago,
                    'changefreq': page['changefreq'],
                    'priority': page['priority']
                })
                logger.info(f"Added static page: {url}")
            except Exception as e:
                logger.warning(f"Could not generate URL for route {page['route']}: {str(e)}")
                continue
        
        # Add dynamic project pages
        try:
            projects = Project.query.all()
            for project in projects:
                url = url_for('projects.view_project', project_id=project.id, _external=True)
                pages.append({
                    'loc': url,
                    'lastmod': project.updated_at.strftime('%Y-%m-%d'),
                    'changefreq': 'weekly',
                    'priority': '0.7'
                })
                logger.info(f"Added project page: {url}")
        except Exception as e:
            logger.warning(f"Could not add project pages to sitemap: {str(e)}")
        
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
        return Response(f'Error generating sitemap: {str(e)}', status=500)

@seo_bp.route('/robots.txt', methods=['GET'])
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
        return Response(f'Error serving robots.txt: {str(e)}', status=500)
