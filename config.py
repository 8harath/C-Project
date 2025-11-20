import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///warehouse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL query logging

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # WTForms configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    # Pagination
    ITEMS_PER_PAGE = 20

    # File upload (for future enhancements)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Reorder level default
    DEFAULT_REORDER_LEVEL = 10

    # Categories
    MEDICINE_CATEGORIES = [
        'Allergy',
        'Cold and Mild Flu',
        'Cough',
        'Dermatology',
        'Eye/ENT',
        'Fever',
        'Pain Relief',
        'Vitamins',
        'Women Hygiene'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
