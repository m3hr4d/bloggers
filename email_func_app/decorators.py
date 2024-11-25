from functools import wraps
from flask import abort
from flask_login import current_user

def check_user_type(required_type):
    """
    A decorator that checks if the current user has the required type.
    :param required_type: The required user type ('influencer' or 'business')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.user_type != required_type:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
