from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from email_func_app.models.message import Message
from email_func_app.extensions import db

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/check_unread')
@login_required
def check_unread():
    """Check for unread messages."""
    unread_count = Message.query.filter_by(
        recipient_id=current_user.id,
        is_read=False
    ).count()
    
    return jsonify({
        'status': 'success',
        'unread_count': unread_count
    })
