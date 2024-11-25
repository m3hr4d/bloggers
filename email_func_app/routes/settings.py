from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from email_func_app.forms.settings import NotificationPreferencesForm, PrivacySettingsForm
from email_func_app.models.user import User
from email_func_app.extensions import db

settings = Blueprint('settings', __name__)

@settings.route('/notifications', methods=['GET', 'POST'])
@login_required
def notification_preferences():
    form = NotificationPreferencesForm()
    
    if form.validate_on_submit():
        # Update user's notification preferences
        current_user.email_notifications = form.email_notifications.data
        current_user.sms_notifications = form.sms_notifications.data
        current_user.new_offers_notifications = form.new_offers.data
        current_user.message_notifications = form.messages.data
        current_user.campaign_notifications = form.campaign_updates.data
        current_user.marketing_notifications = form.marketing_emails.data
        
        db.session.commit()
        flash('Your notification preferences have been updated.', 'success')
        return redirect(url_for('profile.view_profile'))
    
    # Pre-populate form with current settings
    if not form.is_submitted():
        form.email_notifications.data = current_user.email_notifications
        form.sms_notifications.data = current_user.sms_notifications
        form.new_offers.data = current_user.new_offers_notifications
        form.messages.data = current_user.message_notifications
        form.campaign_updates.data = current_user.campaign_notifications
        form.marketing_emails.data = current_user.marketing_notifications
    
    return render_template('profile/notifications.html', form=form)

@settings.route('/privacy', methods=['GET', 'POST'])
@login_required
def privacy_settings():
    form = PrivacySettingsForm()
    
    if form.validate_on_submit():
        # Update user's privacy settings
        current_user.profile_visibility = form.profile_visibility.data
        current_user.show_contact_info = form.show_contact_info.data
        current_user.show_analytics = form.show_analytics.data
        current_user.allow_messages = form.allow_messages.data
        
        db.session.commit()
        flash('Your privacy settings have been updated.', 'success')
        return redirect(url_for('profile.view_profile'))
    
    # Pre-populate form with current settings
    if not form.is_submitted():
        form.profile_visibility.data = current_user.profile_visibility
        form.show_contact_info.data = current_user.show_contact_info
        form.show_analytics.data = current_user.show_analytics
        form.allow_messages.data = current_user.allow_messages
    
    return render_template('profile/privacy.html', form=form)
