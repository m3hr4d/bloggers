from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from email_func_app import db
from email_func_app.models import User, Plan, Offer
from email_func_app.forms import SettingsForm
from email_func_app.main import main
import os

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

@main.route('/dashboard')
@login_required
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

    return render_template(
        'dashboard.html',
        user_type=current_user.user_type,
        plans=plans,
        active_plans=active_plans,
        available_plans=available_plans,
        offers=offers,
        successful_collaborations=successful_collaborations
    )

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    
    if request.method == 'GET':
        # Pre-fill form with current user data
        form.location.data = current_user.location
        
        if current_user.user_type == 'influencer':
            form.phone_number.data = getattr(current_user, 'phone_number', None)
            form.bio.data = getattr(current_user, 'bio', None)
            form.services_interested_in.data = getattr(current_user, 'services_interested_in', None)
        else:
            form.business_website.data = current_user.business_website
    
    if form.validate_on_submit():
        # Verify current password if trying to change password
        if form.new_password.data:
            if not check_password_hash(current_user.password, form.current_password.data):
                flash('رمز عبور فعلی اشتباه است.', 'error')
                return redirect(url_for('main.settings'))
            current_user.password = generate_password_hash(form.new_password.data)
        
        # Update editable fields
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
    
    return render_template('settings.html', 
                         form=form,
                         user_type=current_user.user_type)

@main.route('/search_plans')
@login_required
def search_plans():
    if current_user.user_type != 'business':
        flash('این صفحه فقط برای کسب‌وکارها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))
    return render_template('search_plans.html')

@main.route('/create-plan')
@login_required
def create_plan():
    if current_user.user_type != 'influencer':
        flash('این صفحه فقط برای اینفلوئنسرها در دسترس است.', 'error')
        return redirect(url_for('main.dashboard'))
    return render_template('create_plan.html')
