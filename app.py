from flask import Flask, render_template
from flask_login import LoginManager
from config import config
from models import db
from models.user import User

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create database tables
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")

    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.staff import staff_bp
    from routes.shared import shared_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(shared_bp)

    # Home route
    @app.route('/')
    def home():
        return render_template('home.html')

    return app

if __name__ == '__main__':
    app = create_app('development')
    print("\n" + "="*50)
    print("WAREHOUSE INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("Phase 1: Project Setup Complete ✓")
    print("Phase 2: Authentication System Complete ✓")
    print("Phase 3: Medicine Management Complete ✓")
    print("Starting Flask Development Server...")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
