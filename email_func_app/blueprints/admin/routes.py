from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from . import admin
from email_func_app.models import User, Plan, Offer
from email_func_app import db

def admin_required(f):
    """Decorator to require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard."""
    total_users = User.query.count()
    total_plans = Plan.query.count()
    total_offers = Offer.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_plans = Plan.query.order_by(Plan.created_at.desc()).limit(5).all()
    recent_offers = Offer.query.order_by(Offer.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
        total_users=total_users,
        total_plans=total_plans,
        total_offers=total_offers,
        recent_users=recent_users,
        recent_plans=recent_plans,
        recent_offers=recent_offers
    )

@admin.route('/users')
@login_required
@admin_required
def users():
    """List all users."""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/user/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    """View user details."""
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)

@admin.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.users'))
        
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/user/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(user_id):
    """Toggle user active status."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'error')
        return redirect(url_for('admin.users'))
        
    user.is_active = not user.is_active
    db.session.commit()
    flash(f'User {"activated" if user.is_active else "deactivated"} successfully.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))

@admin.route('/plans')
@login_required
@admin_required
def plans():
    """List all plans."""
    plans = Plan.query.all()
    return render_template('admin/plans.html', plans=plans)

@admin.route('/offers')
@login_required
@admin_required
def offers():
    """List all offers."""
    offers = Offer.query.all()
    return render_template('admin/offers.html', offers=offers)
