"""Main routes for the application."""
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from . import main
from email_func_app.models import User, Plan, Offer, Message, Niche, Service
from email_func_app import db
from email_func_app.forms.plan import PlanForm
from datetime import datetime

@main.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route."""
    # Get stats for the dashboard
    if current_user.is_influencer():
        followers_count = current_user.followers_count or 0
        active_plans = Plan.query.filter_by(influencer_id=current_user.id, status='active').count()
        new_offers = Offer.query.join(Plan).filter(
            Plan.influencer_id == current_user.id,
            Offer.status == 'pending'
        ).count()
        engagement_rate = current_user.engagement_rate or 0.0
    else:
        active_plans = Offer.query.filter_by(business_id=current_user.id, status='accepted').count()
        new_offers = 0  # Businesses don't receive offers
        followers_count = 0  # Not applicable for businesses
        engagement_rate = 0.0  # Not applicable for businesses
    
    # Get unread messages count
    unread_messages = Message.query.filter_by(recipient_id=current_user.id, read=False).count()
    
    return render_template('dashboard.html',
        followers_count=followers_count,
        active_plans=active_plans,
        new_offers=new_offers,
        engagement_rate=engagement_rate,
        unread_messages=unread_messages
    )

@main.route('/influencers')
def influencers():
    """List all influencers."""
    influencers = User.query.filter_by(user_type='influencer').all()
    return render_template('influencers.html', influencers=influencers)

@main.route('/businesses')
def businesses():
    """List all businesses."""
    businesses = User.query.filter_by(user_type='business').all()
    return render_template('brands.html', businesses=businesses)

@main.route('/plans')
def plans():
    """View all travel plans."""
    plans = Plan.query.order_by(Plan.created_at.desc()).all()
    return render_template('plans.html', plans=plans)

@main.route('/plan/<int:plan_id>')
def plan_detail(plan_id):
    """View plan details."""
    plan = Plan.query.get_or_404(plan_id)
    return render_template('view_plan.html', plan=plan)

@main.route('/create-plan', methods=['GET', 'POST'])
@login_required
def create_plan():
    """Create a new travel plan."""
    if not current_user.is_influencer():
        flash('Only influencers can create travel plans.', 'error')
        return redirect(url_for('main.index'))
    
    form = PlanForm()
    
    # Get all niches and services for the form choices
    niches = Niche.query.filter_by(is_active=True).all()
    services = Service.query.filter_by(is_active=True).all()
    
    form.niches.choices = [(n.id, n.name) for n in niches]
    form.services.choices = [(s.id, s.name) for s in services]
    
    if form.validate_on_submit():
        try:
            # Convert date strings to datetime objects
            start_date = datetime.strptime(form.start_date.data, '%Y-%m-%d')
            end_date = datetime.strptime(form.end_date.data, '%Y-%m-%d')
            
            # Create new plan
            plan = Plan(
                influencer_id=current_user.id,
                title=form.title.data,
                description=form.description.data,
                location=form.location.data,
                start_date=start_date,
                end_date=end_date
            )
            
            # Set optional fields
            plan.available_times = form.available_times.data
            plan.content_suggestions = form.content_suggestions.data
            plan.suggested_price = form.suggested_price.data
            plan.additional_notes = form.additional_notes.data
            plan.custom_services = form.custom_services.data
            
            # Add selected niches and services
            if form.niches.data:
                selected_niches = Niche.query.filter(Niche.id.in_(form.niches.data)).all()
                plan.niches.extend(selected_niches)
            
            if form.services.data:
                selected_services = Service.query.filter(Service.id.in_(form.services.data)).all()
                plan.services.extend(selected_services)
            
            # Save to database
            db.session.add(plan)
            db.session.commit()
            
            flash('برنامه با موفقیت ایجاد شد.', 'success')
            return jsonify({'status': 'success', 'redirect': url_for('main.plan_detail', plan_id=plan.id)})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    return render_template('create_plan.html', form=form)

@main.route('/profile/<int:user_id>')
def profile(user_id):
    """View user profile."""
    user = User.query.get_or_404(user_id)
    if user.is_influencer():
        return render_template('influencer_profile.html', influencer=user)
    elif user.is_business():
        return render_template('brand_profile.html', business=user)
    return redirect(url_for('main.index'))

@main.route('/opportunities')
@login_required
def opportunities():
    """View opportunities."""
    return render_template('opportunities.html')

@main.route('/portfolio')
@login_required
def portfolio():
    """View portfolio."""
    return render_template('portfolio.html')

@main.route('/search-plans')
def search_plans():
    """Search travel plans."""
    return render_template('search_plans.html')

@main.route('/campaigns')
@login_required
def campaigns():
    """View campaigns."""
    return render_template('campaigns.html')

@main.route('/messages')
@login_required
def messages():
    """View and manage messages."""
    # Get all messages for the current user (both sent and received)
    received_messages = Message.query.filter_by(recipient_id=current_user.id)\
        .order_by(Message.created_at.desc()).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id)\
        .order_by(Message.created_at.desc()).all()
    
    # Get all tickets (messages without a parent)
    tickets = Message.query.filter(
        Message.parent_id.is_(None),
        db.or_(
            Message.sender_id == current_user.id,
            Message.recipient_id == current_user.id
        )
    ).order_by(Message.created_at.desc()).all()
    
    # Mark all received messages as read
    for message in received_messages:
        if not message.read:
            message.read = True
    db.session.commit()
    
    return render_template('messages.html',
        received_messages=received_messages,
        sent_messages=sent_messages,
        tickets=tickets
    )

@main.route('/messages/<int:message_id>')
@login_required
def view_message(message_id):
    """View a specific message."""
    message = Message.query.get_or_404(message_id)
    
    # Check if user has permission to view this message
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        flash('You do not have permission to view this message.', 'error')
        return redirect(url_for('main.messages'))
    
    # Mark message as read if recipient is viewing
    if message.recipient_id == current_user.id and not message.read:
        message.read = True
        db.session.commit()
    
    return render_template('view_message.html', message=message)

@main.route('/messages/<int:message_id>/reply', methods=['POST'])
@login_required
def reply_message(message_id):
    """Reply to a message."""
    parent_message = Message.query.get_or_404(message_id)
    
    # Check if user has permission to reply
    if parent_message.sender_id != current_user.id and parent_message.recipient_id != current_user.id:
        flash('You do not have permission to reply to this message.', 'error')
        return redirect(url_for('main.messages'))
    
    # Get reply content
    body = request.form.get('body')
    if not body:
        flash('Reply cannot be empty.', 'error')
        return redirect(url_for('main.view_message', message_id=message_id))
    
    # Create reply message
    reply = Message(
        sender_id=current_user.id,
        recipient_id=parent_message.sender_id if parent_message.sender_id != current_user.id else parent_message.recipient_id,
        subject=f"Re: {parent_message.subject}",
        body=body,
        parent_id=message_id if parent_message.parent_id is None else parent_message.parent_id,
        status=parent_message.status
    )
    
    try:
        db.session.add(reply)
        db.session.commit()
        flash('Reply sent successfully!', 'success')
    except:
        db.session.rollback()
        flash('Error sending reply. Please try again.', 'error')
    
    return redirect(url_for('main.view_message', message_id=message_id))

@main.route('/messages/<int:message_id>/status', methods=['POST'])
@login_required
def update_message_status(message_id):
    """Update message status."""
    message = Message.query.get_or_404(message_id)
    
    # Check if user has permission to update status
    if message.sender_id != current_user.id and message.recipient_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403
    
    data = request.get_json()
    status = data.get('status')
    
    if status not in ['pending', 'in_progress', 'resolved', 'closed']:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    
    try:
        message.status = status
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Database error'}), 500

@main.route('/messages/send', methods=['GET', 'POST'])
@login_required
def send_message():
    """Send a new message."""
    if request.method == 'POST':
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        body = request.form.get('body')
        
        if not all([recipient_id, subject, body]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('main.messages'))
            
        try:
            recipient = User.query.get(recipient_id)
            if not recipient:
                flash('Recipient not found.', 'error')
                return redirect(url_for('main.messages'))
                
            message = Message(
                sender_id=current_user.id,
                recipient_id=recipient_id,
                subject=subject,
                body=body
            )
            db.session.add(message)
            db.session.commit()
            
            flash('Message sent successfully!', 'success')
            return redirect(url_for('main.messages'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error sending message. Please try again.', 'error')
            return redirect(url_for('main.messages'))
    
    # GET request - show form
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('send_message.html', users=users)

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User settings."""
    from email_func_app.forms.settings import ProfileSettingsForm, SecuritySettingsForm
    
    profile_form = ProfileSettingsForm(obj=current_user)
    security_form = SecuritySettingsForm()
    
    if request.method == 'POST':
        if 'profile_submit' in request.form and profile_form.validate_on_submit():
            # Check if Instagram profile has changed
            old_instagram = current_user.instagram_profile
            new_instagram = profile_form.instagram_profile.data
            
            # Update profile settings
            profile_form.populate_obj(current_user)
            
            # If Instagram profile has changed, sync the profile
            if old_instagram != new_instagram and new_instagram:
                if current_user.sync_instagram_profile():
                    flash('پروفایل اینستاگرام با موفقیت به‌روزرسانی شد', 'success')
                else:
                    flash('خطا در به‌روزرسانی پروفایل اینستاگرام', 'danger')
            
            db.session.commit()
            flash('تنظیمات پروفایل با موفقیت به‌روزرسانی شد', 'success')
            return redirect(url_for('main.settings'))
            
        elif 'security_submit' in request.form and security_form.validate_on_submit():
            # Verify current password
            if current_user.check_password(security_form.current_password.data):
                current_user.set_password(security_form.new_password.data)
                db.session.commit()
                flash('رمز عبور با موفقیت تغییر کرد', 'success')
                return redirect(url_for('main.settings'))
            else:
                flash('رمز عبور فعلی اشتباه است', 'danger')
    
    return render_template('settings.html', 
                         profile_form=profile_form,
                         security_form=security_form)

@main.route('/analytics')
@login_required
def analytics():
    """View analytics."""
    if current_user.is_influencer():
        # Get influencer analytics
        plans = Plan.query.filter_by(influencer_id=current_user.id).all()
        total_offers = Offer.query.join(Plan).filter(Plan.influencer_id == current_user.id).count()
        accepted_offers = Offer.query.join(Plan).filter(
            Plan.influencer_id == current_user.id,
            Offer.status == 'accepted'
        ).count()
        
        return render_template('analytics.html',
            plans=plans,
            total_offers=total_offers,
            accepted_offers=accepted_offers
        )
    else:
        # Get business analytics
        offers = Offer.query.filter_by(business_id=current_user.id).all()
        total_campaigns = len(offers)
        active_campaigns = sum(1 for o in offers if o.status == 'accepted')
        
        return render_template('analytics.html',
            offers=offers,
            total_campaigns=total_campaigns,
            active_campaigns=active_campaigns
        )
