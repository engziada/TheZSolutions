from functools import wraps
from flask import abort, request, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            if request.is_xhr:
                abort(403)
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def developer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_developer:
            if request.is_xhr:
                abort(403)
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
