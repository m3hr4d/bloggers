from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from . import admin
from email_func_app import db
from email_func_app.models import User

@admin.route('/unverified_users')
@login_required
def unverified_users():
    # Check if current user is admin
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز.', 'danger')
        return redirect(url_for('main.dashboard'))
    users = User.query.filter_by(is_verified=False).all()
    return render_template('admin/unverified_users.html', users=users)

@admin.route('/verify_user/<int:user_id>')
@login_required
def verify_user(user_id):
    # Check if current user is admin
    if not current_user.is_admin:
        flash('دسترسی غیرمجاز.', 'danger')
        return redirect(url_for('main.dashboard'))
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    flash('کاربر با موفقیت تأیید شد.', 'success')
    return redirect(url_for('admin.unverified_users'))
