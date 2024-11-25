from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from email_func_app import db
from email_func_app.models import User, Plan, Offer
from email_func_app.forms import SettingsForm
from email_func_app.main import main
import os
import json
from sqlalchemy import or_
from functools import wraps

def with_sidebar_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement actual unread messages count
        unread_messages = 0
        template = f(*args, **kwargs)
        if isinstance(template, str):
            return render_template(template, unread_messages=unread_messages)
        return template
    return decorated_function

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/brands')
def brands():
    return render_template('brands.html')

@main.route('/influencers')
def influencers():
    return render_template('influencers.html')

@main.route('/influencers/<username>')
def influencer_profile(username):
    return render_template('influencer_profile.html')

@main.route('/dashboard')
@login_required
@with_sidebar_data
def dashboard():
    plans = None
    available_plans = None
    offers = None
    active_plans = None
    successful_collaborations = None

    if current_user.user_type == 'influencer':
        plans = Plan.query.filter_by(influencer_id=current_user.id).all()
        active_plans = [plan for plan in plans if plan.status != 'completed']
    else:
        available_plans = Plan.query.filter_by(status='در حال انتظار').all()
        offers = Offer.query.filter_by(business_id=current_user.id).all()
        successful_collaborations = [offer for offer in offers if offer.status == 'پذیرفته شده']

    return 'dashboard.html'

@main.route('/brand-profile', methods=['GET', 'POST'])
@login_required
@with_sidebar_data
def brand_profile():
    if current_user.user_type != 'business':
        flash('این صفحه فقط برای کسب‌وکارها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))

    # Initialize form data from current user
    form_data = {
        'business_name': current_user.business_name,
        'location': current_user.location,
        'bio': current_user.bio,
        'interests': json.loads(current_user.interests) if current_user.interests else []
    }

    if request.method == 'POST':
        try:
            # Handle profile image upload
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join('email_func_app/static/profile_pics', filename)
                    file.save(file_path)
                    current_user.profile_image = filename

            # Update basic information
            current_user.business_name = request.form.get('brand_name')
            current_user.location = request.form.get('location')
            current_user.bio = request.form.get('about')

            # Update interests
            interests = request.form.getlist('interests')
            current_user.interests = json.dumps(interests)

            db.session.commit()
            flash('پروفایل برند با موفقیت به‌روزرسانی شد.', 'success')
            
            # Update form data after successful save
            form_data = {
                'business_name': current_user.business_name,
                'location': current_user.location,
                'bio': current_user.bio,
                'interests': interests
            }
        except Exception as e:
            db.session.rollback()
            print(f"Error updating brand profile: {e}")
            flash('خطا در به‌روزرسانی پروفایل. لطفاً دوباره تلاش کنید.', 'error')

    return 'brand_profile.html'

@main.route('/settings', methods=['GET', 'POST'])
@login_required
@with_sidebar_data
def settings():
    form = SettingsForm()
    
    if request.method == 'GET':
        form.location.data = current_user.location
        
        if current_user.user_type == 'influencer':
            form.phone_number.data = getattr(current_user, 'phone_number', None)
            form.bio.data = getattr(current_user, 'bio', None)
            form.services_interested_in.data = getattr(current_user, 'services_interested_in', None)
        else:
            form.business_website.data = current_user.business_website
    
    if form.validate_on_submit():
        if form.new_password.data:
            if not check_password_hash(current_user.password, form.current_password.data):
                flash('رمز عبور فعلی اشتباه است.', 'error')
                return redirect(url_for('main.settings'))
            current_user.password = generate_password_hash(form.new_password.data)
        
        current_user.location = form.location.data
        
        if current_user.user_type == 'influencer':
            current_user.phone_number = form.phone_number.data
            current_user.bio = form.bio.data
            current_user.services_interested_in = form.services_interested_in.data
        else:
            current_user.business_website = form.business_website.data
        
        try:
            db.session.commit()
            flash('تغییرات با موفقیت ذخیره شد.', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error updating settings: {e}")
            flash('خطا در ذخیره تغییرات. لطفاً دوباره تلاش کنید.', 'error')
        
        return redirect(url_for('main.settings'))
    
    return 'settings.html'

@main.route('/search_plans', methods=['GET', 'POST'])
@login_required
@with_sidebar_data
def search_plans():
    if current_user.user_type != 'business':
        flash('این صفحه فقط برای کسب‌وکارها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))

    search_results = None
    if request.method == 'POST':
        location = request.form.get('location', '')
        topics = request.form.get('topics', '')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        query = Plan.query.filter_by(status='در حال انتظار')

        if location:
            query = query.filter(Plan.location.ilike(f'%{location}%'))
        
        if topics:
            query = query.filter(Plan.topics_of_interest.ilike(f'%{topics}%'))
        
        if start_date:
            query = query.filter(Plan.start_date >= start_date)
        
        if end_date:
            query = query.filter(Plan.end_date <= end_date)

        search_results = query.all()

    return 'search_plans.html'

@main.route('/create-plan')
@login_required
@with_sidebar_data
def create_plan():
    if current_user.user_type != 'influencer':
        flash('این صفحه فقط برای اینفلوئنسرها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))
    return 'create_plan.html'

@main.route('/campaigns')
@login_required
@with_sidebar_data
def campaigns():
    if current_user.user_type != 'business':
        flash('این صفحه فقط برای کسب و کارها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))
    return 'campaigns.html'

@main.route('/opportunities')
@login_required
@with_sidebar_data
def opportunities():
    if current_user.user_type != 'influencer':
        flash('این صفحه فقط برای اینفلوئنسرها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))
    return 'opportunities.html'

@main.route('/portfolio')
@login_required
@with_sidebar_data
def portfolio():
    if current_user.user_type != 'influencer':
        flash('این صفحه فقط برای اینفلوئنسرها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))
    return 'portfolio.html'

@main.route('/analytics')
@login_required
@with_sidebar_data
def analytics():
    return 'analytics.html'

@main.route('/messages')
@login_required
@with_sidebar_data
def messages():
    return 'messages.html'
