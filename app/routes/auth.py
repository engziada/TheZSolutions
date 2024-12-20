from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User, CustomerProfile, DeveloperProfile
from app import db, bcrypt
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html', title='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'customer')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(email=email, username=username, role=role)
        user.set_password(password)
        
        db.session.add(user)
        
        # Create corresponding profile based on role
        if role == 'customer':
            profile = CustomerProfile(user=user)
        elif role == 'developer':
            profile = DeveloperProfile(user=user)
        
        db.session.add(profile)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if current_user.role == 'customer':
            profile = current_user.customer_profile
            profile.company_name = request.form.get('company_name')
            profile.industry = request.form.get('industry')
            profile.phone = request.form.get('phone')
            profile.address = request.form.get('address')
        
        elif current_user.role == 'developer':
            profile = current_user.developer_profile
            profile.skills = request.form.getlist('skills[]')
            profile.experience_years = int(request.form.get('experience_years', 0))
            profile.portfolio_url = request.form.get('portfolio_url')
            profile.github_url = request.form.get('github_url')
            profile.linkedin_url = request.form.get('linkedin_url')
            profile.bio = request.form.get('bio')
            profile.hourly_rate = float(request.form.get('hourly_rate', 0))
            profile.availability_status = request.form.get('availability_status')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', title='Profile')
