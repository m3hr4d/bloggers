from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from ..models.user import User, UserVerification, UserAnalytics, SocialMediaAccount, Portfolio
from ..forms.profile import (BasicProfileForm, InfluencerProfileForm, BusinessProfileForm,
                           NotificationPreferencesForm, PrivacySettingsForm,
                           SocialMediaAccountForm, PortfolioItemForm)
from .. import db

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['GET'])
@login_required
def view_profile():
    """View user profile."""
    return render_template('profile/view.html', user=current_user)

@profile.route('/profile/edit/basic', methods=['GET', 'POST'])
@login_required
def edit_basic_profile():
    """Edit basic profile information."""
    form = BasicProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        form.populate_obj(current_user)
        
        if form.profile_image.data:
            filename = secure_filename(form.profile_image.data.filename)
            form.profile_image.data.save(os.path.join('uploads', filename))
            current_user.profile_image = filename
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))
        
    return render_template('profile/edit_basic.html', form=form)

@profile.route('/profile/edit/influencer', methods=['GET', 'POST'])
@login_required
def edit_influencer_profile():
    """Edit influencer-specific profile details."""
    if current_user.account_type != 'influencer':
        flash('Access denied. Influencer account required.', 'error')
        return redirect(url_for('profile.view_profile'))
        
    form = InfluencerProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Influencer profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))
        
    return render_template('profile/edit_influencer.html', form=form)

@profile.route('/profile/edit/business', methods=['GET', 'POST'])
@login_required
def edit_business_profile():
    """Edit business-specific profile details."""
    if current_user.account_type != 'business':
        flash('Access denied. Business account required.', 'error')
        return redirect(url_for('profile.view_profile'))
        
    form = BusinessProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Business profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))
        
    return render_template('profile/edit_business.html', form=form)

@profile.route('/profile/social-media', methods=['GET', 'POST'])
@login_required
def manage_social_media():
    """Manage social media accounts."""
    form = SocialMediaAccountForm()
    
    if form.validate_on_submit():
        account = SocialMediaAccount(
            user_id=current_user.id,
            platform=form.platform.data,
            username=form.username.data,
            profile_url=form.profile_url.data
        )
        db.session.add(account)
        db.session.commit()
        flash('Social media account added successfully!', 'success')
        return redirect(url_for('profile.manage_social_media'))
        
    return render_template('profile/social_media.html', 
                         form=form, 
                         accounts=current_user.social_media_accounts)

@profile.route('/profile/social-media/<int:account_id>', methods=['DELETE'])
@login_required
def delete_social_media(account_id):
    """Delete a social media account."""
    account = SocialMediaAccount.query.get_or_404(account_id)
    if account.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully'})

@profile.route('/profile/portfolio', methods=['GET', 'POST'])
@login_required
def manage_portfolio():
    """Manage portfolio items."""
    form = PortfolioItemForm()
    
    if form.validate_on_submit():
        item = Portfolio(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            media_type=form.media_type.data,
            media_url=form.media_url.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Portfolio item added successfully!', 'success')
        return redirect(url_for('profile.manage_portfolio'))
        
    return render_template('profile/portfolio.html', 
                         form=form, 
                         items=current_user.portfolio_items)

@profile.route('/profile/portfolio/<int:item_id>', methods=['DELETE'])
@login_required
def delete_portfolio_item(item_id):
    """Delete a portfolio item."""
    item = Portfolio.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Portfolio item deleted successfully'})

@profile.route('/profile/settings/notifications', methods=['GET', 'POST'])
@login_required
def notification_settings():
    """Manage notification preferences."""
    form = NotificationPreferencesForm(obj=current_user)
    
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Notification preferences updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))
        
    return render_template('profile/notifications.html', form=form)

@profile.route('/profile/settings/privacy', methods=['GET', 'POST'])
@login_required
def privacy_settings():
    """Manage privacy settings."""
    form = PrivacySettingsForm(obj=current_user)
    
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Privacy settings updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))
        
    return render_template('profile/privacy.html', form=form)

@profile.route('/profile/analytics')
@login_required
def view_analytics():
    """View profile analytics."""
    analytics = UserAnalytics.query.filter_by(user_id=current_user.id).first()
    return render_template('profile/analytics.html', analytics=analytics)

@profile.route('/profile/verification')
@login_required
def verification_status():
    """View verification status and requirements."""
    verification = UserVerification.query.filter_by(user_id=current_user.id).first()
    return render_template('profile/verification.html', verification=verification)
