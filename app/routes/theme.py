from flask import Blueprint, jsonify, request
from app.utils.theme import set_theme, get_theme

theme_bp = Blueprint('theme', __name__)

@theme_bp.route('/api/theme', methods=['GET', 'POST'])
def toggle_theme():
    """Handle theme toggling."""
    if request.method == 'POST':
        new_theme = request.json.get('theme')
        if set_theme(new_theme):
            return jsonify({'status': 'success', 'theme': new_theme})
        return jsonify({'status': 'error', 'message': 'Invalid theme'}), 400
    
    return jsonify({'theme': get_theme()})
