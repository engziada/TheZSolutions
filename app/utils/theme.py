from flask import session

def get_theme():
    """Get the current theme preference."""
    return session.get('theme', 'light')

def set_theme(theme):
    """Set the theme preference."""
    if theme in ['light', 'dark']:
        session['theme'] = theme
        return True
    return False
