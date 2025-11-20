from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models import db, login_manager

class User(UserMixin, db.Model):
    """User model for authentication and authorization"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Staff')  # Admin or Staff
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sales = db.relationship('Sale', backref='user', lazy='dynamic')

    def __init__(self, username, email, password, role='Staff'):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Return the user ID as a string (required by Flask-Login)"""
        return str(self.user_id)

    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'Admin'

    def is_staff(self):
        """Check if user has staff role"""
        return self.role == 'Staff'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))
