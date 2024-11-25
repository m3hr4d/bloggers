from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import offers
from email_func_app.models import User, Plan, Offer
from email_func_app import db

@offers.route('/submit/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def submit_offer(plan_id):
    """Submit an offer for a plan."""
    if not current_user.is_business():
        flash('Only businesses can submit offers.', 'error')
        return redirect(url_for('main.plans'))
        
    plan = Plan.query.get_or_404(plan_id)
    
    if request.method == 'POST':
        offer = Offer(
            business_id=current_user.id,
            plan_id=plan.id,
            description=request.form.get('description'),
            services_offered=request.form.get('services_offered'),
            status='pending'
        )
        
        db.session.add(offer)
        db.session.commit()
        
        flash('Offer submitted successfully!', 'success')
        return redirect(url_for('main.plan_detail', plan_id=plan.id))
        
    return render_template('submit_offer.html', plan=plan)

@offers.route('/view-campaigns')
@login_required
def view_campaigns():
    """View user's campaigns."""
    if current_user.is_business():
        campaigns = Offer.query.filter_by(business_id=current_user.id).all()
    else:
        plans = Plan.query.filter_by(influencer_id=current_user.id).all()
        plan_ids = [plan.id for plan in plans]
        campaigns = Offer.query.filter(Offer.plan_id.in_(plan_ids)).all()
    return render_template('view_campaigns.html', campaigns=campaigns)

@offers.route('/edit-plan/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def edit_plan(plan_id):
    """Edit a plan."""
    plan = Plan.query.get_or_404(plan_id)
    if current_user.id != plan.influencer_id:
        flash('You can only edit your own plans.', 'error')
        return redirect(url_for('main.plans'))
        
    if request.method == 'POST':
        plan.destination = request.form.get('destination', plan.destination)
        plan.location = request.form.get('location', plan.location)
        plan.start_date = request.form.get('start_date', plan.start_date)
        plan.end_date = request.form.get('end_date', plan.end_date)
        plan.time = request.form.get('time', plan.time)
        plan.services_requested = request.form.get('services_requested', plan.services_requested)
        plan.topics_of_interest = request.form.get('topics_of_interest', plan.topics_of_interest)
        
        db.session.commit()
        flash('Plan updated successfully!', 'success')
        return redirect(url_for('main.plan_detail', plan_id=plan.id))
        
    return render_template('create_plan.html', plan=plan, editing=True)

@offers.route('/delete-plan/<int:plan_id>', methods=['POST'])
@login_required
def delete_plan(plan_id):
    """Delete a plan."""
    plan = Plan.query.get_or_404(plan_id)
    if current_user.id != plan.influencer_id:
        flash('You can only delete your own plans.', 'error')
        return redirect(url_for('main.plans'))
        
    db.session.delete(plan)
    db.session.commit()
    flash('Plan deleted successfully!', 'success')
    return redirect(url_for('main.plans'))

@offers.route('/update-offer-status/<int:offer_id>/<status>')
@login_required
def update_offer_status(offer_id, status):
    """Update offer status."""
    offer = Offer.query.get_or_404(offer_id)
    plan = Plan.query.get(offer.plan_id)
    
    if not current_user.is_influencer() or current_user.id != plan.influencer_id:
        flash('You do not have permission to update this offer.', 'error')
        return redirect(url_for('main.index'))
        
    if status in ['accepted', 'rejected']:
        offer.status = status
        db.session.commit()
        flash(f'Offer {status}.', 'success')
    else:
        flash('Invalid status.', 'error')
        
    return redirect(url_for('main.plan_detail', plan_id=plan.id))

@offers.route('/delete-campaign/<int:campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    """Delete a campaign."""
    campaign = Offer.query.get_or_404(campaign_id)
    if current_user.id != campaign.business_id:
        flash('You can only delete your own campaigns.', 'error')
        return redirect(url_for('offers.view_campaigns'))
        
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('offers.view_campaigns'))
