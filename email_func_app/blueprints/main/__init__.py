from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes  # Import routes at the end to avoid circular imports
