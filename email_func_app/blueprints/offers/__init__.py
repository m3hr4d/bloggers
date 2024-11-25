from flask import Blueprint

offers = Blueprint('offers', __name__)

from . import routes
