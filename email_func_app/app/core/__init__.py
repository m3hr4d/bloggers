"""Core functionality package."""
from flask_login import current_user

def check_permission(permission):
    """Check if current user has the required permission."""
    return current_user.is_authenticated and current_user.has_permission(permission)
