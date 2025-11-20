from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db

class User(UserMixin, db.Model):
    """User model for authentication and authorization"""

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Staff')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    sales = db.relationship('Sale', backref='seller', lazy='dynamic')

    def __init__(self, username, email, password, role='Staff'):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'Admin'

    def is_staff(self):
        """Check if user has staff role"""
        return self.role == 'Staff'

    def get_id(self):
        """Required for Flask-Login"""
        return str(self.user_id)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
