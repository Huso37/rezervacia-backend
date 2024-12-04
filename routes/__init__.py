from flask import Blueprint
from routes.auth import auth_bp
from routes.core import core_bp

def init_routes(app):
    """Register all route Blueprints."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(core_bp)