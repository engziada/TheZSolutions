from flask import request, session
from flask_babel import Babel

babel = Babel()

def get_locale():
    # Try to get the language from the session
    if 'language' in session:
        return session['language']
    
    # Try to get the language from the request header
    return request.accept_languages.best_match(['en', 'ar'])

def init_babel(app):
    babel.init_app(app, locale_selector=get_locale)
    return babel 