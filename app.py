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

    # Register blueprints (will add in Phase 2)
    # from routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    # Home route (temporary)
    @app.route('/')
    def home():
        return '''
        <html>
            <head>
                <title>Warehouse Inventory Management</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        text-align: center;
                        background: white;
                        padding: 50px;
                        border-radius: 10px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 10px;
                    }
                    p {
                        color: #666;
                        font-size: 18px;
                    }
                    .status {
                        color: #28a745;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🏥 Warehouse Inventory Management System</h1>
                    <p class="status">✓ Phase 1 Complete - System Initialized</p>
                    <p>Database models created and ready for use.</p>
                    <p><small>Authentication and UI coming in Phase 2...</small></p>
                </div>
            </body>
        </html>
        '''

    return app

if __name__ == '__main__':
    app = create_app('development')
    print("\n" + "="*50)
    print("WAREHOUSE INVENTORY MANAGEMENT SYSTEM")
    print("="*50)
    print("Phase 1: Project Setup Complete ✓")
    print("Starting Flask Development Server...")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
