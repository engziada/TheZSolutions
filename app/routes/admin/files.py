from flask import Blueprint, render_template, request, jsonify, send_file, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.project import Project, ProjectFile
from app.utils.file_manager import FileManager
from app.utils.decorators import admin_required
from app import db
import os
from flask_babel import _

bp = Blueprint('admin_files', __name__)

@bp.route('/project/<int:project_id>/files')
@login_required
@admin_required
def project_files(project_id):
    project = Project.query.get_or_404(project_id)
    files = ProjectFile.query.filter_by(project_id=project_id).all()
    categories = FileManager.ALLOWED_EXTENSIONS.keys()
    
    return render_template('admin/files.html',
                         project=project,
                         files=files,
                         categories=categories)

@bp.route('/file/upload', methods=['POST'])
@login_required
@admin_required
def upload_file():
    try:
        if 'files' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400
            
        files = request.files.getlist('files')
        project_id = request.form.get('project_id')
        category = request.form.get('category')
        description = request.form.get('description')
        is_public = request.form.get('is_public') == 'true'
        
        uploaded_files = []
        for file in files:
            if file.filename == '':
                continue
                
            try:
                # Save file using FileManager
                file_path = FileManager.save_file(file, project_id, category)
                
                # Create database record
                project_file = ProjectFile(
                    project_id=project_id,
                    file=file,
                    uploaded_by=current_user.id,
                    description=description,
                    category=category,
                    is_public=is_public
                )
                
                db.session.add(project_file)
                uploaded_files.append(project_file)
                
            except Exception as e:
                # Clean up any files that were uploaded before the error
                for uploaded_file in uploaded_files:
                    FileManager.delete_file(uploaded_file.file_path)
                db.session.rollback()
                raise e
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'{len(uploaded_files)} files uploaded successfully'})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/file/<int:file_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
@admin_required
def manage_file(file_id):
    file = ProjectFile.query.get_or_404(file_id)
    
    if request.method == 'GET':
        return jsonify(file.to_dict())
        
    elif request.method == 'POST':
        try:
            # Update file metadata
            file.description = request.form.get('description', file.description)
            file.category = request.form.get('category', file.category)
            file.is_public = request.form.get('is_public') == 'true'
            
            # If new file is provided, update the file
            if 'file' in request.files:
                new_file = request.files['file']
                if new_file.filename != '':
                    # Delete old file
                    FileManager.delete_file(file.file_path)
                    
                    # Save new file
                    file_path = FileManager.save_file(new_file, file.project_id, file.category)
                    file.increment_version()
                    
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'File updated successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
            
    elif request.method == 'DELETE':
        try:
            # Delete file from filesystem
            FileManager.delete_file(file.file_path)
            
            # Delete database record
            db.session.delete(file)
            db.session.commit()
            
            return jsonify({'status': 'success', 'message': 'File deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/file/<int:file_id>/download')
@login_required
def download_file(file_id):
    file = ProjectFile.query.get_or_404(file_id)
    
    # Check if user has access to the file
    if not file.is_public and not current_user.is_admin:
        return jsonify({'status': 'error', 'message': 'Access denied'}), 403
    
    try:
        # Increment download count
        file.increment_download_count()
        
        # Send file
        return send_file(
            file.get_absolute_path(),
            as_attachment=True,
            download_name=file.original_filename
        )
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
