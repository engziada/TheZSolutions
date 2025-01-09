from flask import Blueprint, send_file, flash, redirect, url_for, current_app
from app.models.application import Application
from app.decorators import admin_required
import os
from flask_babel import _

bp = Blueprint('downloads', __name__)

@bp.route('/cv/<int:application_id>')
@admin_required
def download_cv(application_id):
    try:
        application = Application.query.get_or_404(application_id)
        
        if not application.resume_path:
            flash(_('No CV file found for this application.'), 'error')
            return redirect(url_for('admin.application_detail', id=application_id))
        
        # Get the absolute path to the file
        file_path = os.path.abspath(os.path.join(current_app.config['RESUMES_FOLDER'], application.resume_path))
        current_app.logger.info(f'Attempting to download CV from path: {file_path}')
        
        if not os.path.exists(file_path):
            current_app.logger.error(f'CV file not found at path: {file_path}')
            flash(_('No CV file found for this application.'), 'error')
            return redirect(url_for('admin.application_detail', id=application_id))
        
        try:
            current_app.logger.info(f'Sending file: {file_path}')
            return send_file(
                file_path,
                as_attachment=True,
                download_name=application.resume_path
            )
        except Exception as e:
            current_app.logger.error(f'Error sending file: {str(e)}')
            flash(_('Error downloading the file. Please try again.'), 'error')
            return redirect(url_for('admin.application_detail', id=application_id))
            
    except Exception as e:
        current_app.logger.error(f'Error in download_cv: {str(e)}')
        flash(_('An unexpected error occurred.'), 'error')
        return redirect(url_for('admin.application_detail', id=application_id)) 