"""Offers blueprint package."""
from flask import Blueprint

offers_bp = Blueprint('offers', __name__, template_folder='templates')

from . import routes  # noqa
