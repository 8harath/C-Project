import os
from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db, login_manager

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.medicine import medicine_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(medicine_bp, url_prefix='/medicines')

    # Create database tables
    with app.app_context():
        db.create_all()

    # Home route
    @app.route('/')
    def index():
        """Home page"""
        return render_template('home.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
