import os
import shutil
from werkzeug.utils import secure_filename
from flask import current_app
import hashlib
from datetime import datetime
import logging
import mimetypes

logger = logging.getLogger(__name__)

class FileManager:
    ALLOWED_EXTENSIONS = {
        'document': {'pdf', 'doc', 'docx', 'txt', 'rtf', 'odt'},
        'image': {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg'},
        'source_code': {'py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'h', 'php'},
        'archive': {'zip', 'rar', '7z', 'tar', 'gz'},
        'spreadsheet': {'xls', 'xlsx', 'csv'},
        'presentation': {'ppt', 'pptx'},
    }

    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

    @staticmethod
    def get_file_category(filename):
        """Determine file category based on extension"""
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        for category, extensions in FileManager.ALLOWED_EXTENSIONS.items():
            if ext in extensions:
                return category
        return 'other'

    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        all_extensions = set()
        for extensions in FileManager.ALLOWED_EXTENSIONS.values():
            all_extensions.update(extensions)
        return ext in all_extensions

    @staticmethod
    def get_file_hash(file):
        """Generate SHA-256 hash of file content"""
        sha256_hash = hashlib.sha256()
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
        file.seek(0)
        return sha256_hash.hexdigest()

    @staticmethod
    def get_mime_type(file_path):
        """Get MIME type of file using mimetypes module"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            # Default to application/octet-stream if type cannot be determined
            return 'application/octet-stream'
        return mime_type

    @staticmethod
    def create_upload_directory(project_id, category=None):
        """Create directory structure for file upload"""
        base_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'projects',
            str(project_id)
        )
        if category:
            base_path = os.path.join(base_path, category)

        os.makedirs(base_path, exist_ok=True)
        return base_path

    @staticmethod
    def save_file(file, project_id, category=None):
        """Save uploaded file to appropriate directory"""
        try:
            if not file:
                raise ValueError("No file provided")

            # Check file size
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)

            if size > FileManager.MAX_FILE_SIZE:
                raise ValueError(f"File size exceeds maximum limit of {FileManager.MAX_FILE_SIZE/1024/1024}MB")

            # Secure filename and check extension
            filename = secure_filename(file.filename)
            if not FileManager.allowed_file(filename):
                raise ValueError("File type not allowed")

            # Create directory
            upload_dir = FileManager.create_upload_directory(project_id, category)

            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name, ext = os.path.splitext(filename)
            unique_filename = f"{base_name}_{timestamp}{ext}"
            file_path = os.path.join(upload_dir, unique_filename)

            # Save file
            file.save(file_path)

            # Verify MIME type
            mime_type = FileManager.get_mime_type(file_path)
            if 'text' not in mime_type and 'application' not in mime_type and 'image' not in mime_type:
                os.remove(file_path)
                raise ValueError("Invalid file type")

            return file_path

        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise

    @staticmethod
    def delete_file(file_path):
        """Delete file from filesystem"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)

                # Remove empty parent directories
                directory = os.path.dirname(file_path)
                while directory != current_app.config['UPLOAD_FOLDER']:
                    if not os.listdir(directory):
                        os.rmdir(directory)
                    directory = os.path.dirname(directory)

                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise

    @staticmethod
    def move_file(source_path, dest_path):
        """Move file to new location"""
        try:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(source_path, dest_path)
            return True
        except Exception as e:
            logger.error(f"Error moving file: {str(e)}")
            raise

    @staticmethod
    def copy_file(source_path, dest_path):
        """Copy file to new location"""
        try:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(source_path, dest_path)
            return True
        except Exception as e:
            logger.error(f"Error copying file: {str(e)}")
            raise

    @staticmethod
    def get_file_info(file_path):
        """Get file information"""
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_ctime),
                'modified_at': datetime.fromtimestamp(stat.st_mtime),
                'mime_type': FileManager.get_mime_type(file_path),
                'hash': FileManager.get_file_hash(open(file_path, 'rb'))
            }
        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            raise

    @staticmethod
    def validate_file_integrity(file_path, original_hash):
        """Validate file integrity using hash"""
        try:
            current_hash = FileManager.get_file_hash(open(file_path, 'rb'))
            return current_hash == original_hash
        except Exception as e:
            logger.error(f"Error validating file integrity: {str(e)}")
            raise
