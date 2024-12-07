from flask import Blueprint

core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def home():
    return "Welcome to the App! Use the APIs for authentication and management."
