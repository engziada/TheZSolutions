from flask import Blueprint
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

# Import routes
from app.routes.admin import portfolio

# Register sub-blueprints
admin_bp.register_blueprint(portfolio.portfolio_bp, url_prefix='/portfolio')

# Import routes after blueprint creation to avoid circular imports
from app.routes.admin import routes
