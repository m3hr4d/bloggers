from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from email_func_app import db
from email_func_app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'business' and not current_user.onboarding_completed:
            return redirect(url_for('auth.onboarding', step=1))
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            print(f"Login attempt - Email: {email}")
            
            user = User.query.filter_by(email=email).first()
            if not user:
                print(f"No user found with email: {email}")
                flash('ایمیل یا رمز عبور اشتباه است.', 'danger')
                return render_template('login.html')
            
            print(f"User found - Type: {user.user_type}")
            is_valid = check_password_hash(user.password, password)
            print(f"Password valid: {is_valid}")
            
            if is_valid:
                try:
                    # Set session permanent and add user info
                    session.permanent = True
                    session['user_id'] = user.id
                    session['user_email'] = user.email
                    session['user_type'] = user.user_type
                    
                    # Login user with remember me
                    login_user(user, remember=True)
                    print(f"Login successful for user: {email}")
                    
                    # Clear any existing flash messages
                    session.pop('_flashes', None)
                    
                    if user.user_type == 'business' and not user.onboarding_completed:
                        return redirect(url_for('auth.onboarding', step=1))
                    
                    next_page = request.args.get('next')
                    if next_page and next_page != url_for('auth.login'):
                        return redirect(next_page)
                    return redirect(url_for('main.dashboard'))
                except Exception as e:
                    print(f"Error during login_user: {str(e)}")
                    db.session.rollback()
                    flash('خطا در ورود به سیستم. لطفا دوباره تلاش کنید.', 'danger')
            else:
                flash('ایمیل یا رمز عبور اشتباه است.', 'danger')
        except Exception as e:
            print(f"Login error: {str(e)}")
            db.session.rollback()
            flash('خطا در ورود به سیستم. لطفا دوباره تلاش کنید.', 'danger')
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        if User.query.filter_by(email=email).first():
            flash('این ایمیل قبلاً ثبت شده است.', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            user_type=user_type
        )
        
        # Add additional fields based on user type
        if user_type == 'business':
            user.business_name = request.form.get('business_name')
            user.business_website = request.form.get('website')
            user.business_type = request.form.get('business_type')
        else:
            user.name = request.form.get('name')
            user.instagram_profile = request.form.get('instagram')
            user.followers = request.form.get('followers')
        
        try:
            db.session.add(user)
            db.session.commit()
            
            if user_type == 'business':
                login_user(user)
                return redirect(url_for('auth.onboarding', step=1))
            
            flash('ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.', 'danger')
    
    return render_template('register.html')

@auth.route('/onboarding/<int:step>', methods=['GET', 'POST'])
@login_required
def onboarding(step):
    if current_user.user_type != 'business' or current_user.onboarding_completed:
        return redirect(url_for('main.dashboard'))
    
    total_steps = 5
    
    if step < 1 or step > total_steps:
        return redirect(url_for('auth.onboarding', step=1))
    
    if request.method == 'POST':
        try:
            if step == 1:
                current_user.industry = request.form.get('industry')
            elif step == 2:
                categories = request.form.getlist('categories')
                current_user.categories = ','.join(categories)
            elif step == 3:
                current_user.experience_level = request.form.get('experience')
            elif step == 4:
                current_user.content_needs = request.form.get('content_needs')
            elif step == 5:
                current_user.annual_budget = request.form.get('budget')
                current_user.onboarding_completed = True
            
            db.session.commit()
            
            if step == total_steps:
                flash('اطلاعات شما با موفقیت ثبت شد.', 'success')
                return redirect(url_for('main.dashboard'))
            
            return redirect(url_for('auth.onboarding', step=step + 1))
            
        except Exception as e:
            db.session.rollback()
            flash('خطا در ثبت اطلاعات. لطفاً دوباره تلاش کنید.', 'danger')
    
    return render_template('onboarding.html', step=step, total_steps=total_steps)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
