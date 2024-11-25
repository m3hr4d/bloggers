"""Plan routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from email_func_app.forms.plan import PlanForm
from email_func_app.models.plan import Plan
from email_func_app.models.niche import Niche, Service
from email_func_app.extensions import db
from datetime import datetime

bp = Blueprint('plans', __name__)

@bp.route('/create-plan', methods=['GET', 'POST'])
@login_required
def create_plan():
    """Create a new plan."""
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
                end_date=end_date,
                available_times=form.available_times.data,
                content_suggestions=form.content_suggestions.data,
                suggested_price=form.suggested_price.data,
                additional_notes=form.additional_notes.data,
                custom_services=form.custom_services.data
            )
            
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
            return jsonify({'status': 'success', 'redirect': url_for('plans.view_plan', plan_id=plan.id)})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    # If GET request or form validation failed, render template
    return render_template('create_plan.html', 
                         form=form,
                         niches=niches,
                         services=services,
                         current_user=current_user)
