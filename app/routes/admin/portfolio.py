from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app.models.portfolio import PortfolioProject, PortfolioImage
from app.models.user import User
from app import db
from app.utils.decorators import admin_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask_babel import _

# Create a blueprint for portfolio management
portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/projects')
@admin_required
def projects():
    """Display all portfolio projects"""
    page = request.args.get('page', 1, type=int)
    projects = PortfolioProject.query.order_by(PortfolioProject.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/portfolio/projects.html', projects=projects)

@portfolio_bp.route('/projects/new', methods=['GET', 'POST'])
@admin_required
def new_project():
    """Create a new portfolio project"""
    if request.method == 'POST':
        try:
            # Log form data for debugging
            current_app.logger.info("Processing new project form submission")
            current_app.logger.info(f"Form keys: {list(request.form.keys())}")
            
            title = request.form.get('title')
            description = request.form.get('description', '')
            
            # Log data sizes for debugging
            current_app.logger.info(f"Title length: {len(title) if title else 0}")
            current_app.logger.info(f"Description length: {len(description) if description else 0}")
            
            is_active = 'is_active' in request.form

            # Create new project
            project = PortfolioProject(
                title=title,
                description=description,
                is_active=is_active,
                added_by=current_user.id
            )

            db.session.add(project)
            db.session.commit()

            # Handle image uploads
            # Check for all possible file input names
            all_images = []
            if 'images' in request.files:
                all_images.extend(request.files.getlist('images'))
            if 'images[]' in request.files:
                all_images.extend(request.files.getlist('images[]'))
            if 'file-upload' in request.files:
                all_images.extend(request.files.getlist('file-upload'))

            current_app.logger.info(f"Found {len(all_images)} images to process")

            if all_images:
                # Create directory for project images if it doesn't exist
                project_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'portfolio', str(project.id))
                os.makedirs(project_dir, exist_ok=True)

                # Process all images
                is_first_image = True  # Track if this is the first image overall
                processed_images = 0

                for image in all_images:
                    if image and image.filename:
                        try:
                            # Set the first image as primary by default
                            is_primary = is_first_image
                            is_first_image = False  # Only the first image will be primary

                            # Create image record
                            portfolio_image = PortfolioImage(
                                project_id=project.id,
                                file=image,
                                is_primary=is_primary
                            )

                            db.session.add(portfolio_image)

                            # Save the file - convert path to use forward slashes
                            image_path = os.path.join(project_dir, portfolio_image.filename).replace('\\', '/')
                            image.save(image_path)

                            processed_images += 1
                            current_app.logger.info(f"Saved image: {image.filename} to {image_path}")
                        except Exception as img_error:
                            current_app.logger.error(f"Error processing image {image.filename}: {str(img_error)}")
                
                current_app.logger.info(f"Successfully processed {processed_images} images")
                db.session.commit()

            flash(_('Project added successfully!'), 'success')
            return redirect(url_for('admin.portfolio.projects'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating project: {str(e)}")
            flash(_('An error occurred while creating the project. Please try again.'), 'danger')
            return render_template('admin/portfolio/new_project.html')

    return render_template('admin/portfolio/new_project.html')

@portfolio_bp.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_project(id):
    """Edit an existing portfolio project"""
    project = PortfolioProject.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.is_active = 'is_active' in request.form

        # Handle image uploads
        # Check for all possible file input names
        all_images = []
        if 'images' in request.files:
            all_images.extend(request.files.getlist('images'))
        if 'images[]' in request.files:
            all_images.extend(request.files.getlist('images[]'))
        if 'file-upload' in request.files:
            all_images.extend(request.files.getlist('file-upload'))

        if all_images:
            # Create directory for project images if it doesn't exist
            project_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'portfolio', str(project.id))
            os.makedirs(project_dir, exist_ok=True)

            # Check if this is the first image for the project
            has_primary = PortfolioImage.query.filter_by(project_id=project.id, is_primary=True).first() is not None

            for image in all_images:
                if image and image.filename:
                    # If no primary image exists, set the first uploaded image as primary
                    is_primary = False
                    if not has_primary:
                        is_primary = True
                        has_primary = True

                    # Create image record
                    portfolio_image = PortfolioImage(
                        project_id=project.id,
                        file=image,
                        is_primary=is_primary
                    )

                    db.session.add(portfolio_image)

                    # Save the file - convert path to use forward slashes
                    image_path = os.path.join(project_dir, portfolio_image.filename).replace('\\', '/')
                    image.save(image_path)

                    print(f"Saved image in edit: {image.filename} to {image_path}")

        db.session.commit()
        flash(_('Project updated successfully!'), 'success')
        return redirect(url_for('admin.portfolio.projects'))

    return render_template('admin/portfolio/edit_project.html', project=project)

@portfolio_bp.route('/projects/<int:id>/view')
@admin_required
def view_project(id):
    """View a portfolio project's details"""
    project = PortfolioProject.query.get_or_404(id)
    return render_template('admin/portfolio/view_project.html', project=project)

@portfolio_bp.route('/projects/<int:id>/delete', methods=['POST'])
@admin_required
def delete_project(id):
    """Delete a portfolio project"""
    project = PortfolioProject.query.get_or_404(id)

    # Delete project images from filesystem
    for image in project.images:
        image_path = os.path.join(current_app.root_path, 'static', image.file_path)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete project from database (cascade will delete images)
    db.session.delete(project)
    db.session.commit()

    flash(_('Project deleted successfully!'), 'success')
    return redirect(url_for('admin.portfolio.projects'))

@portfolio_bp.route('/projects/images/<int:id>/delete', methods=['POST'])
@admin_required
def delete_image(id):
    """Delete a project image"""
    image = PortfolioImage.query.get_or_404(id)
    project_id = image.project_id

    # Delete image from filesystem
    image_path = os.path.join(current_app.root_path, 'static', image.file_path)
    if os.path.exists(image_path):
        os.remove(image_path)

    # Delete image from database
    db.session.delete(image)

    # If this was the primary image, set another image as primary if available
    if image.is_primary:
        remaining_image = PortfolioImage.query.filter_by(project_id=project_id).first()
        if remaining_image:
            remaining_image.is_primary = True

    db.session.commit()

    return jsonify({'status': 'success'})

@portfolio_bp.route('/projects/images/<int:id>/set-primary', methods=['POST'])
@admin_required
def set_primary_image(id):
    """Set an image as the primary image for a project"""
    image = PortfolioImage.query.get_or_404(id)

    # Clear primary flag on all images for this project
    for proj_image in PortfolioImage.query.filter_by(project_id=image.project_id).all():
        proj_image.is_primary = False

    # Set this image as primary
    image.is_primary = True
    db.session.commit()

    return jsonify({'status': 'success'})
