from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth
from email_func_app.models import User
from email_func_app import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
            
        flash('Invalid email or password.', 'error')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html')
            
        user = User(
            email=email,
            password=generate_password_hash(password),
            user_type=user_type
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User settings."""
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.bio = request.form.get('bio', current_user.bio)
        current_user.location = request.form.get('location', current_user.location)
        current_user.website = request.form.get('website', current_user.website)
        
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename:
                # Handle profile image upload
                pass
                
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.settings'))
        
    return render_template('auth/settings.html')

@auth.route('/onboarding/<int:step>', methods=['GET', 'POST'])
@login_required
def onboarding(step):
    """User onboarding process."""
    total_steps = 3
    
    if request.method == 'POST':
        if step == 1:
            current_user.name = request.form.get('name')
            current_user.bio = request.form.get('bio')
        elif step == 2:
            current_user.location = request.form.get('location')
            current_user.website = request.form.get('website')
        elif step == 3:
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file.filename:
                    # Handle profile image upload
                    pass
                    
        db.session.commit()
        
        if step < total_steps:
            return redirect(url_for('auth.onboarding', step=step + 1))
        return redirect(url_for('main.dashboard'))
        
    return render_template('auth/onboarding.html', step=step, total_steps=total_steps)
