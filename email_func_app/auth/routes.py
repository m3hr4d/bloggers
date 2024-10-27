from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from email_func_app import db
from email_func_app.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('ایمیل یا رمز عبور اشتباه است.', 'danger')
    
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
            password=generate_password_hash(password),
            user_type=user_type
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.', 'danger')
    
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
