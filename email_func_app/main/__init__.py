from flask import Blueprint

main = Blueprint('main', __name__)

from email_func_app.main import routes
