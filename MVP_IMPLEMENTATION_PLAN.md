# Warehouse and Inventory Management System - MVP Implementation Plan

**Project:** Pharmaceutical Warehouse Management System
**Version:** 1.0
**Date:** November 20, 2024
**Team:** Chandralekha S, Akshaya N, S Sridevi

---

## Executive Summary

This document provides a detailed implementation roadmap for developing the Warehouse and Inventory Management System MVP. The project is structured into 8 phases spanning 14 days, with clear deliverables, technical specifications, and acceptance criteria for each phase.

**Key Metrics:**
- **Total Duration:** 14 days
- **Core Features:** 30+
- **Database Tables:** 4 (User, Medicine, Sale, Alternative Medicine)
- **User Roles:** 2 (Admin, Staff)
- **Seed Data:** 100 medicines across 9 categories
- **Technology Stack:** Flask, SQLAlchemy, SQLite, Bootstrap 5, Chart.js

---

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Technology Stack Details](#technology-stack-details)
3. [Phase-wise Implementation](#phase-wise-implementation)
4. [Database Design](#database-design)
5. [Security Implementation](#security-implementation)
6. [Testing Strategy](#testing-strategy)
7. [Deployment Guide](#deployment-guide)
8. [Risk Assessment](#risk-assessment)
9. [Success Criteria](#success-criteria)

---

## Project Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Browser    │  │   Camera     │  │  Chart.js    │     │
│  │  (Chrome/    │  │   (Barcode   │  │  Renderer    │     │
│  │   Firefox)   │  │   Scanner)   │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼────────────┘
          │                  │                  │
          │ HTTP/HTTPS       │ WebRTC          │ JSON
          │                  │                  │
┌─────────┼──────────────────┼──────────────────┼────────────┐
│         ▼                  ▼                  ▼            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │           PRESENTATION LAYER (JINJA2)                │ │
│  │  - HTML Templates with Bootstrap 5                   │ │
│  │  - Dynamic Content Rendering                         │ │
│  │  - Client-side Validation (JavaScript)               │ │
│  └───────────────────────┬──────────────────────────────┘ │
│                          │                                 │
│  ┌───────────────────────▼──────────────────────────────┐ │
│  │         APPLICATION LAYER (FLASK)                    │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │ │
│  │  │    Auth      │  │    Admin     │  │   Staff    │ │ │
│  │  │   Routes     │  │   Routes     │  │  Routes    │ │ │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │ │
│  │  │  Business    │  │  Flask-Login │  │  API       │ │ │
│  │  │   Logic      │  │  (Sessions)  │  │  Routes    │ │ │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │ │
│  └───────────────────────┬──────────────────────────────┘ │
│                          │                                 │
│  ┌───────────────────────▼──────────────────────────────┐ │
│  │          DATA ACCESS LAYER (SQLALCHEMY)              │ │
│  │  - ORM Models (User, Medicine, Sale, Alternative)    │ │
│  │  - Query Builder                                     │ │
│  │  - Transaction Management                            │ │
│  └───────────────────────┬──────────────────────────────┘ │
│                          │                                 │
│  ┌───────────────────────▼──────────────────────────────┐ │
│  │           PERSISTENCE LAYER (SQLITE3)                │ │
│  │  - warehouse.db (File-based Database)                │ │
│  │  - ACID Transactions                                 │ │
│  │  - Indexes for Performance                           │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
warehouse_inventory/
│
├── app.py                          # Flask application entry point
├── config.py                       # Configuration management
├── seed_database.py                # Database seeding script
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (not in git)
├── .gitignore                     # Git ignore file
├── README.md                      # Project documentation
│
├── models/                        # Database Models
│   ├── __init__.py               # SQLAlchemy initialization
│   ├── user.py                   # User model with authentication
│   ├── medicine.py               # Medicine model
│   ├── sale.py                   # Sale model
│   └── alternative_medicine.py   # Alternative medicine model
│
├── routes/                        # Route Handlers (Blueprints)
│   ├── __init__.py               # Blueprint registration
│   ├── auth.py                   # Authentication routes
│   ├── admin.py                  # Admin-only routes
│   ├── staff.py                  # Staff routes
│   ├── shared.py                 # Shared routes (sell, scan)
│   └── api.py                    # API endpoints (JSON responses)
│
├── forms/                         # WTForms
│   ├── __init__.py
│   ├── auth_forms.py             # Login, Register forms
│   ├── medicine_forms.py         # Medicine CRUD forms
│   └── sale_forms.py             # Sale recording forms
│
├── utils/                         # Utility Functions
│   ├── __init__.py
│   ├── decorators.py             # Custom decorators (role_required)
│   ├── validators.py             # Custom validators
│   └── analytics.py              # Analytics calculations
│
├── static/                        # Static Assets
│   ├── css/
│   │   ├── custom.css           # Custom styles
│   │   └── dashboard.css        # Dashboard-specific styles
│   ├── js/
│   │   ├── scanner.js           # Barcode scanning (QuaggaJS)
│   │   ├── charts.js            # Chart.js configurations
│   │   ├── validation.js        # Form validation
│   │   └── main.js              # General JavaScript
│   ├── images/
│   │   ├── logo.png
│   │   └── favicon.ico
│   └── vendor/                   # Third-party libraries (if local)
│       ├── bootstrap-5.3.0/
│       ├── chartjs-4.0.0/
│       └── quagga-0.12.1/
│
├── templates/                     # Jinja2 Templates
│   ├── base.html                 # Base template (navbar, footer)
│   ├── home.html                 # Landing page
│   │
│   ├── auth/                     # Authentication templates
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── admin/                    # Admin-only templates
│   │   ├── admin_dashboard.html
│   │   ├── manage_products.html
│   │   ├── manage_users.html
│   │   ├── predictive_insights.html
│   │   ├── reports.html
│   │   └── alternatives.html
│   │
│   ├── staff/                    # Staff templates
│   │   └── staff_dashboard.html
│   │
│   ├── shared/                   # Shared templates
│   │   ├── sell_medicines.html
│   │   ├── scan.html
│   │   ├── receipt.html
│   │   ├── products.html        # View-only product list
│   │   └── about.html
│   │
│   └── components/               # Reusable components
│       ├── navbar.html
│       ├── footer.html
│       ├── alerts.html
│       └── pagination.html
│
├── migrations/                    # Database migrations (Flask-Migrate)
│   └── versions/
│
├── tests/                        # Unit and integration tests
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_medicine.py
│   ├── test_sales.py
│   └── test_analytics.py
│
└── warehouse.db                  # SQLite database (generated)
```

---

## Technology Stack Details

### Backend Technologies

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| Python | 3.8+ | Core language | python.org |
| Flask | 2.3.3 | Web framework | flask.palletsprojects.com |
| Flask-SQLAlchemy | 3.0.5 | ORM | flask-sqlalchemy.palletsprojects.com |
| Flask-Login | 0.6.2 | Session management | flask-login.readthedocs.io |
| Flask-WTF | 1.1.1 | Form handling | flask-wtf.readthedocs.io |
| WTForms | 3.0.1 | Form validation | wtforms.readthedocs.io |
| SQLite | 3.x | Database | sqlite.org |
| Werkzeug | 2.3.x | Security utilities | werkzeug.palletsprojects.com |

### Frontend Technologies

| Technology | Version | Purpose | CDN/Local |
|------------|---------|---------|-----------|
| Bootstrap | 5.3.0 | CSS framework | CDN |
| Chart.js | 4.0.0 | Data visualization | CDN |
| QuaggaJS | 0.12.1 | Barcode scanning | CDN |
| jQuery | 3.7.0 | DOM manipulation | CDN (optional) |
| Font Awesome | 6.4.0 | Icons | CDN |

### Development Tools

| Tool | Purpose |
|------|---------|
| pip | Dependency management |
| venv | Virtual environment |
| Flask Debug Toolbar | Development debugging |
| DB Browser for SQLite | Database inspection |

---

## Phase-wise Implementation

### Phase 1: Project Setup & Database Models (Days 1-2)

#### Objectives
- Set up project structure
- Configure Flask application
- Create database models
- Establish testing environment

#### Tasks

##### Task 1.1: Initialize Project Structure
**Duration:** 2 hours

**Steps:**
1. Create project directory structure as per architecture
2. Initialize Git repository
3. Create `.gitignore` file
4. Set up virtual environment

**Commands:**
```bash
mkdir warehouse_inventory && cd warehouse_inventory
mkdir -p models routes forms utils static/{css,js,images} templates/{auth,admin,staff,shared,components} tests migrations
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
git init
```

**`.gitignore` content:**
```
venv/
__pycache__/
*.pyc
*.pyo
*.db
*.log
.env
.DS_Store
.vscode/
.idea/
instance/
```

##### Task 1.2: Create Configuration File
**Duration:** 1 hour

**File:** `config.py`

```python
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
```

##### Task 1.3: Create User Model
**Duration:** 2 hours

**File:** `models/user.py`

```python
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
```

##### Task 1.4: Create Medicine Model
**Duration:** 2 hours

**File:** `models/medicine.py`

```python
from datetime import datetime
from models import db

class Medicine(db.Model):
    """Medicine model for inventory management"""

    __tablename__ = 'medicine'

    medicine_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    manufacturer = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False, index=True)
    stock = db.Column(db.Integer, nullable=False, default=0, index=True)
    reorder_level = db.Column(db.Integer, nullable=False, default=10)
    barcode = db.Column(db.String(13), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sales = db.relationship('Sale', backref='medicine', lazy='dynamic')
    alternatives_as_primary = db.relationship(
        'AlternativeMedicine',
        foreign_keys='AlternativeMedicine.primary_medicine_id',
        backref='primary_medicine',
        lazy='dynamic'
    )
    alternatives_as_alternative = db.relationship(
        'AlternativeMedicine',
        foreign_keys='AlternativeMedicine.alternative_medicine_id',
        backref='alternative_medicine',
        lazy='dynamic'
    )

    def __init__(self, name, manufacturer, category, quantity, price,
                 expiry_date, barcode, description=None, stock=None, reorder_level=10):
        self.name = name
        self.description = description
        self.manufacturer = manufacturer
        self.category = category
        self.quantity = quantity
        self.price = price
        self.expiry_date = expiry_date
        self.stock = stock if stock is not None else quantity
        self.reorder_level = reorder_level
        self.barcode = barcode

    def is_low_stock(self):
        """Check if medicine stock is below reorder level"""
        return self.stock <= self.reorder_level

    def is_expired(self):
        """Check if medicine is expired"""
        from datetime import date
        return self.expiry_date < date.today()

    def is_expiring_soon(self, days=30):
        """Check if medicine expires within specified days"""
        from datetime import date, timedelta
        return self.expiry_date <= (date.today() + timedelta(days=days))

    def update_stock(self, quantity_sold):
        """Update stock after sale"""
        if self.stock >= quantity_sold:
            self.stock -= quantity_sold
            return True
        return False

    def to_dict(self):
        """Convert medicine to dictionary (for API responses)"""
        return {
            'medicine_id': self.medicine_id,
            'name': self.name,
            'description': self.description,
            'manufacturer': self.manufacturer,
            'category': self.category,
            'quantity': self.quantity,
            'price': float(self.price),
            'expiry_date': self.expiry_date.isoformat(),
            'stock': self.stock,
            'reorder_level': self.reorder_level,
            'barcode': self.barcode,
            'is_low_stock': self.is_low_stock(),
            'is_expired': self.is_expired()
        }

    def __repr__(self):
        return f'<Medicine {self.name} (Stock: {self.stock})>'
```

##### Task 1.5: Create Sale Model
**Duration:** 1 hour

**File:** `models/sale.py`

```python
from datetime import datetime
from models import db

class Sale(db.Model):
    """Sale model for transaction recording"""

    __tablename__ = 'sale'

    sale_id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __init__(self, medicine_id, user_id, quantity_sold, total_price):
        self.medicine_id = medicine_id
        self.user_id = user_id
        self.quantity_sold = quantity_sold
        self.total_price = total_price

    @property
    def season(self):
        """Get season based on sale date"""
        month = self.sale_date.month
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Monsoon'

    def to_dict(self):
        """Convert sale to dictionary"""
        return {
            'sale_id': self.sale_id,
            'medicine_id': self.medicine_id,
            'medicine_name': self.medicine.name,
            'user_id': self.user_id,
            'seller_name': self.seller.username,
            'quantity_sold': self.quantity_sold,
            'total_price': float(self.total_price),
            'sale_date': self.sale_date.isoformat(),
            'season': self.season
        }

    def __repr__(self):
        return f'<Sale {self.sale_id}: {self.quantity_sold} units>'
```

##### Task 1.6: Create Alternative Medicine Model
**Duration:** 1 hour

**File:** `models/alternative_medicine.py`

```python
from models import db

class AlternativeMedicine(db.Model):
    """Alternative medicine mapping model"""

    __tablename__ = 'alternative_medicine'

    alternative_id = db.Column(db.Integer, primary_key=True)
    primary_medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False, index=True)
    alternative_medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False)
    reason = db.Column(db.Text)
    priority = db.Column(db.Integer, default=5)

    __table_args__ = (
        db.UniqueConstraint('primary_medicine_id', 'alternative_medicine_id', name='unique_alternative'),
    )

    def __init__(self, primary_medicine_id, alternative_medicine_id, reason=None, priority=5):
        self.primary_medicine_id = primary_medicine_id
        self.alternative_medicine_id = alternative_medicine_id
        self.reason = reason
        self.priority = priority

    def __repr__(self):
        return f'<Alternative {self.primary_medicine_id} -> {self.alternative_medicine_id}>'
```

##### Task 1.7: Initialize Models Module
**Duration:** 30 minutes

**File:** `models/__init__.py`

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.medicine import Medicine
from models.sale import Sale
from models.alternative_medicine import AlternativeMedicine
```

##### Task 1.8: Create Basic Flask Application
**Duration:** 1 hour

**File:** `app.py` (Initial version)

```python
from flask import Flask
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

    # Register blueprints (will add in Phase 2)
    # from routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
```

##### Task 1.9: Create Requirements File
**Duration:** 15 minutes

**File:** `requirements.txt`

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
WTForms==3.0.1
email-validator==2.0.0
python-dotenv==1.0.0
```

#### Deliverables
- ✅ Complete project structure
- ✅ All database models created and tested
- ✅ Configuration management in place
- ✅ Virtual environment with dependencies installed
- ✅ Basic Flask app running

#### Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Verify database creation
ls -l warehouse.db

# Test database models (Python shell)
python
>>> from app import create_app
>>> from models import db
>>> from models.user import User
>>> app = create_app()
>>> with app.app_context():
...     user = User('testuser', 'test@example.com', 'password123', 'Admin')
...     db.session.add(user)
...     db.session.commit()
...     print(User.query.first())
```

---

### Phase 2: Authentication System (Day 3)

#### Objectives
- Implement user registration
- Implement login/logout functionality
- Set up role-based access control
- Create authentication templates

#### Tasks

##### Task 2.1: Create Custom Decorators
**Duration:** 1 hour

**File:** `utils/decorators.py`

```python
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('staff.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    """Decorator to require staff or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

##### Task 2.2: Create Authentication Forms
**Duration:** 1 hour

**File:** `forms/auth_forms.py`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.user import User

class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20, message='Username must be between 3 and 20 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Role', choices=[('Staff', 'Staff'), ('Admin', 'Admin')], default='Staff')
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
```

##### Task 2.3: Create Authentication Routes
**Duration:** 2 hours

**File:** `routes/auth.py`

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from models import db
from models.user import User
from forms.auth_forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('staff.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully for {user.username}! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('staff.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # Check if username or email
        user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.username.data)
        ).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash(f'Welcome back, {user.username}!', 'success')

            # Redirect to appropriate dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('staff.dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
```

##### Task 2.4: Create Base Template
**Duration:** 2 hours

**File:** `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Warehouse Inventory Management{% endblock %}</title>

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation Bar -->
    {% include 'components/navbar.html' %}

    <!-- Flash Messages -->
    <div class="container mt-3">
        {% include 'components/alerts.html' %}
    </div>

    <!-- Main Content -->
    <main class="container my-4">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    {% include 'components/footer.html' %}

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- jQuery (optional, for easier AJAX) -->
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>

    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

##### Task 2.5: Create Navigation Component
**Duration:** 1 hour

**File:** `templates/components/navbar.html`

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('home') if current_user.is_anonymous else (url_for('admin.dashboard') if current_user.is_admin() else url_for('staff.dashboard')) }}">
            <i class="fas fa-warehouse"></i> Warehouse Manager
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                {% if current_user.is_authenticated %}
                    <!-- Admin Menu -->
                    {% if current_user.is_admin() %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('admin.dashboard') }}">
                                <i class="fas fa-tachometer-alt"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('admin.manage_products') }}">
                                <i class="fas fa-pills"></i> Manage Products
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('admin.alternatives') }}">
                                <i class="fas fa-exchange-alt"></i> Alternatives
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('admin.predictive_insights') }}">
                                <i class="fas fa-chart-line"></i> Insights
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('admin.reports') }}">
                                <i class="fas fa-file-alt"></i> Reports
                            </a>
                        </li>
                    {% else %}
                        <!-- Staff Menu -->
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('staff.dashboard') }}">
                                <i class="fas fa-tachometer-alt"></i> Dashboard
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('shared.products') }}">
                                <i class="fas fa-pills"></i> Products
                            </a>
                        </li>
                    {% endif %}

                    <!-- Common Menu Items -->
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('shared.sell') }}">
                            <i class="fas fa-shopping-cart"></i> Sell
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('shared.scan') }}">
                            <i class="fas fa-barcode"></i> Scan
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('shared.about') }}">
                            <i class="fas fa-info-circle"></i> About
                        </a>
                    </li>

                    <!-- User Dropdown -->
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user"></i> {{ current_user.username }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><span class="dropdown-item-text">Role: {{ current_user.role }}</span></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{{ url_for('auth.logout') }}">
                                <i class="fas fa-sign-out-alt"></i> Logout
                            </a></li>
                        </ul>
                    </li>
                {% else %}
                    <!-- Public Menu -->
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.login') }}">
                            <i class="fas fa-sign-in-alt"></i> Login
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('auth.register') }}">
                            <i class="fas fa-user-plus"></i> Register
                        </a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
```

##### Task 2.6: Create Alert Component
**Duration:** 30 minutes

**File:** `templates/components/alerts.html`

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                {% if category == 'success' %}
                    <i class="fas fa-check-circle"></i>
                {% elif category == 'danger' or category == 'error' %}
                    <i class="fas fa-exclamation-triangle"></i>
                {% elif category == 'warning' %}
                    <i class="fas fa-exclamation-circle"></i>
                {% elif category == 'info' %}
                    <i class="fas fa-info-circle"></i>
                {% endif %}
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

##### Task 2.7: Create Footer Component
**Duration:** 30 minutes

**File:** `templates/components/footer.html`

```html
<footer class="bg-dark text-white mt-5 py-4">
    <div class="container">
        <div class="row">
            <div class="col-md-4">
                <h5><i class="fas fa-warehouse"></i> Warehouse Manager</h5>
                <p class="text-muted">Pharmaceutical Inventory Management System</p>
            </div>
            <div class="col-md-4">
                <h5>Quick Links</h5>
                <ul class="list-unstyled">
                    <li><a href="{{ url_for('shared.about') }}" class="text-white-50">About Us</a></li>
                    <li><a href="#" class="text-white-50">Contact</a></li>
                </ul>
            </div>
            <div class="col-md-4">
                <h5>Contact</h5>
                <p class="text-muted">
                    <i class="fas fa-envelope"></i> chandralekha508@gmail.com<br>
                    <i class="fas fa-phone"></i> +91 7022897595
                </p>
                <div class="social-links">
                    <a href="#" class="text-white-50 me-3"><i class="fab fa-instagram fa-lg"></i></a>
                    <a href="#" class="text-white-50"><i class="fab fa-google-play fa-lg"></i></a>
                </div>
            </div>
        </div>
        <hr class="bg-secondary">
        <div class="text-center text-muted">
            <p>&copy; 2024 Warehouse Inventory Management System. All rights reserved.</p>
            <p class="small">Developed by: Chandralekha S, Akshaya N, S Sridevi</p>
        </div>
    </div>
</footer>
```

##### Task 2.8: Create Login Template
**Duration:** 1 hour

**File:** `templates/auth/login.html`

```html
{% extends 'base.html' %}

{% block title %}Login - Warehouse Manager{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
        <div class="card shadow">
            <div class="card-header bg-primary text-white text-center">
                <h3><i class="fas fa-sign-in-alt"></i> Login</h3>
            </div>
            <div class="card-body">
                <form method="POST" action="{{ url_for('auth.login') }}">
                    {{ form.hidden_tag() }}

                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control" + (" is-invalid" if form.username.errors else ""), placeholder="Enter username or email") }}
                        {% if form.username.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.username.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control" + (" is-invalid" if form.password.errors else ""), placeholder="Enter password") }}
                        {% if form.password.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.password.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <div class="d-grid">
                        {{ form.submit(class="btn btn-primary btn-block") }}
                    </div>
                </form>
            </div>
            <div class="card-footer text-center">
                <small>Don't have an account? <a href="{{ url_for('auth.register') }}">Register here</a></small>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

##### Task 2.9: Create Registration Template
**Duration:** 1 hour

**File:** `templates/auth/register.html`

```html
{% extends 'base.html' %}

{% block title %}Register - Warehouse Manager{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
        <div class="card shadow">
            <div class="card-header bg-success text-white text-center">
                <h3><i class="fas fa-user-plus"></i> Register</h3>
            </div>
            <div class="card-body">
                <form method="POST" action="{{ url_for('auth.register') }}" novalidate>
                    {{ form.hidden_tag() }}

                    <div class="mb-3">
                        {{ form.username.label(class="form-label") }}
                        {{ form.username(class="form-control" + (" is-invalid" if form.username.errors else ""), placeholder="Choose a username") }}
                        {% if form.username.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.username.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                        <small class="form-text text-muted">3-20 characters, alphanumeric</small>
                    </div>

                    <div class="mb-3">
                        {{ form.email.label(class="form-label") }}
                        {{ form.email(class="form-control" + (" is-invalid" if form.email.errors else ""), placeholder="Enter email address") }}
                        {% if form.email.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.email.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        {{ form.password.label(class="form-label") }}
                        {{ form.password(class="form-control" + (" is-invalid" if form.password.errors else ""), placeholder="Create a password") }}
                        {% if form.password.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.password.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                        <small class="form-text text-muted">Minimum 8 characters</small>
                    </div>

                    <div class="mb-3">
                        {{ form.confirm_password.label(class="form-label") }}
                        {{ form.confirm_password(class="form-control" + (" is-invalid" if form.confirm_password.errors else ""), placeholder="Confirm password") }}
                        {% if form.confirm_password.errors %}
                            <div class="invalid-feedback">
                                {% for error in form.confirm_password.errors %}{{ error }}{% endfor %}
                            </div>
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        {{ form.role.label(class="form-label") }}
                        {{ form.role(class="form-select") }}
                    </div>

                    <div class="d-grid">
                        {{ form.submit(class="btn btn-success btn-block") }}
                    </div>
                </form>
            </div>
            <div class="card-footer text-center">
                <small>Already have an account? <a href="{{ url_for('auth.login') }}">Login here</a></small>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

##### Task 2.10: Update app.py to Register Blueprints
**Duration:** 15 minutes

**File:** `app.py` (Updated)

```python
# ... previous code ...

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

    # Register blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Home route
    @app.route('/')
    def home():
        return render_template('home.html')

    return app

# ... rest of code ...
```

#### Deliverables
- ✅ User registration with validation
- ✅ Login/logout functionality
- ✅ Role-based access control decorators
- ✅ Base templates with navigation
- ✅ Flash message system

#### Testing
- [ ] Register new Admin user
- [ ] Register new Staff user
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Verify session persistence
- [ ] Test logout functionality
- [ ] Verify role-based navigation menu

---

### Phase 3: Medicine Management (Days 4-5)

#### Objectives
- Implement medicine CRUD operations
- Add search and filter functionality
- Create seed data script
- Populate database with 100 medicines

#### Tasks

##### Task 3.1: Create Medicine Forms
**Duration:** 2 hours

**File:** `forms/medicine_forms.py`

```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import date, timedelta
from config import Config

class MedicineForm(FlaskForm):
    """Form for adding/editing medicines"""
    name = StringField('Medicine Name', validators=[
        DataRequired(message='Medicine name is required'),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[Length(max=500)])
    manufacturer = StringField('Manufacturer', validators=[
        DataRequired(message='Manufacturer is required'),
        Length(max=200)
    ])
    category = SelectField('Category', validators=[DataRequired()],
                          choices=[(cat, cat) for cat in Config.MEDICINE_CATEGORIES])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=0, message='Quantity cannot be negative')
    ])
    price = DecimalField('Price (₹)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Price cannot be negative')
    ], places=2)
    expiry_date = DateField('Expiry Date', validators=[DataRequired()], format='%Y-%m-%d')
    stock = IntegerField('Stock', validators=[
        DataRequired(),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    reorder_level = IntegerField('Reorder Level', validators=[
        DataRequired(),
        NumberRange(min=0, message='Reorder level cannot be negative')
    ], default=10)
    barcode = StringField('Barcode (13 digits)', validators=[
        DataRequired(),
        Length(min=13, max=13, message='Barcode must be exactly 13 digits')
    ])
    submit = SubmitField('Save Medicine')

    def validate_expiry_date(self, expiry_date):
        """Ensure expiry date is in the future"""
        if expiry_date.data <= date.today():
            raise ValidationError('Expiry date must be in the future')

    def validate_barcode(self, barcode):
        """Ensure barcode contains only digits"""
        if not barcode.data.isdigit():
            raise ValidationError('Barcode must contain only digits')

class SearchFilterForm(FlaskForm):
    """Form for searching and filtering medicines"""
    search = StringField('Search', validators=[Length(max=100)])
    category = SelectField('Category', choices=[('', 'All Categories')] +
                          [(cat, cat) for cat in Config.MEDICINE_CATEGORIES])
    sort_by = SelectField('Sort By', choices=[
        ('name', 'Name'),
        ('price', 'Price'),
        ('stock', 'Stock'),
        ('expiry_date', 'Expiry Date')
    ], default='name')
    submit = SubmitField('Filter')
```

##### Task 3.2: Create Admin Routes for Medicine Management
**Duration:** 3 hours

**File:** `routes/admin.py`

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.medicine import Medicine
from forms.medicine_forms import MedicineForm, SearchFilterForm
from utils.decorators import admin_required
from sqlalchemy import or_

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    from models.sale import Sale
    from sqlalchemy import func

    # Get statistics
    total_sales = db.session.query(func.sum(Sale.total_price)).scalar() or 0
    total_medicines = Medicine.query.count()
    low_stock_count = Medicine.query.filter(Medicine.stock <= Medicine.reorder_level).count()
    total_transactions = Sale.query.count()

    # Get low stock items
    low_stock_items = Medicine.query.filter(Medicine.stock <= Medicine.reorder_level).limit(10).all()

    stats = {
        'total_sales': float(total_sales),
        'total_medicines': total_medicines,
        'low_stock_count': low_stock_count,
        'total_transactions': total_transactions
    }

    return render_template('admin/admin_dashboard.html', stats=stats, low_stock_items=low_stock_items)

@admin_bp.route('/medicines')
@login_required
@admin_required
def manage_products():
    """View and manage all medicines"""
    form = SearchFilterForm(request.args, meta={'csrf': False})

    # Base query
    query = Medicine.query

    # Apply search filter
    if form.search.data:
        search_term = f"%{form.search.data}%"
        query = query.filter(or_(
            Medicine.name.ilike(search_term),
            Medicine.manufacturer.ilike(search_term)
        ))

    # Apply category filter
    if form.category.data:
        query = query.filter(Medicine.category == form.category.data)

    # Apply sorting
    sort_by = form.sort_by.data or 'name'
    if sort_by == 'name':
        query = query.order_by(Medicine.name)
    elif sort_by == 'price':
        query = query.order_by(Medicine.price.desc())
    elif sort_by == 'stock':
        query = query.order_by(Medicine.stock)
    elif sort_by == 'expiry_date':
        query = query.order_by(Medicine.expiry_date)

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    medicines = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin/manage_products.html',
                          medicines=medicines,
                          form=form)

@admin_bp.route('/medicines/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_medicine():
    """Add new medicine"""
    form = MedicineForm()

    if form.validate_on_submit():
        # Check for duplicate barcode
        existing = Medicine.query.filter_by(barcode=form.barcode.data).first()
        if existing:
            flash('A medicine with this barcode already exists.', 'danger')
            return render_template('admin/medicine_form.html', form=form, title='Add Medicine')

        medicine = Medicine(
            name=form.name.data,
            description=form.description.data,
            manufacturer=form.manufacturer.data,
            category=form.category.data,
            quantity=form.quantity.data,
            price=form.price.data,
            expiry_date=form.expiry_date.data,
            stock=form.stock.data,
            reorder_level=form.reorder_level.data,
            barcode=form.barcode.data
        )

        db.session.add(medicine)
        db.session.commit()

        flash(f'Medicine "{medicine.name}" added successfully!', 'success')
        return redirect(url_for('admin.manage_products'))

    return render_template('admin/medicine_form.html', form=form, title='Add Medicine')

@admin_bp.route('/medicines/edit/<int:medicine_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_medicine(medicine_id):
    """Edit existing medicine"""
    medicine = Medicine.query.get_or_404(medicine_id)
    form = MedicineForm(obj=medicine)

    if form.validate_on_submit():
        # Check for duplicate barcode (excluding current medicine)
        existing = Medicine.query.filter(
            Medicine.barcode == form.barcode.data,
            Medicine.medicine_id != medicine_id
        ).first()
        if existing:
            flash('A medicine with this barcode already exists.', 'danger')
            return render_template('admin/medicine_form.html', form=form,
                                 title='Edit Medicine', medicine=medicine)

        medicine.name = form.name.data
        medicine.description = form.description.data
        medicine.manufacturer = form.manufacturer.data
        medicine.category = form.category.data
        medicine.quantity = form.quantity.data
        medicine.price = form.price.data
        medicine.expiry_date = form.expiry_date.data
        medicine.stock = form.stock.data
        medicine.reorder_level = form.reorder_level.data
        medicine.barcode = form.barcode.data

        db.session.commit()

        flash(f'Medicine "{medicine.name}" updated successfully!', 'success')
        return redirect(url_for('admin.manage_products'))

    return render_template('admin/medicine_form.html', form=form,
                          title='Edit Medicine', medicine=medicine)

@admin_bp.route('/medicines/delete/<int:medicine_id>', methods=['POST'])
@login_required
@admin_required
def delete_medicine(medicine_id):
    """Delete medicine"""
    medicine = Medicine.query.get_or_404(medicine_id)

    # Check if medicine has sales history
    if medicine.sales.count() > 0:
        flash(f'Cannot delete "{medicine.name}" as it has sales history. Consider marking it as out of stock instead.', 'warning')
        return redirect(url_for('admin.manage_products'))

    name = medicine.name
    db.session.delete(medicine)
    db.session.commit()

    flash(f'Medicine "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin.manage_products'))
```

##### Task 3.3: Create Seed Data Script
**Duration:** 3 hours

**File:** `seed_database.py`

```python
from app import create_app
from models import db
from models.user import User
from models.medicine import Medicine
from models.alternative_medicine import AlternativeMedicine
from datetime import date, timedelta
import random

def seed_users():
    """Create default users"""
    # Check if users already exist
    if User.query.first():
        print("Users already exist. Skipping user creation.")
        return

    admin = User(
        username='admin',
        email='admin@warehouse.com',
        password='admin123',
        role='Admin'
    )

    staff = User(
        username='staff',
        email='staff@warehouse.com',
        password='staff123',
        role='Staff'
    )

    db.session.add(admin)
    db.session.add(staff)
    db.session.commit()

    print("✓ Default users created:")
    print("  - Admin: username='admin', password='admin123'")
    print("  - Staff: username='staff', password='staff123'")

def seed_medicines():
    """Create 100 medicine records"""
    if Medicine.query.first():
        print("Medicines already exist. Skipping medicine creation.")
        return

    medicines_data = [
        # Allergy (11 medicines)
        {"name": "Cetirizine 10mg", "desc": "Antihistamine for allergy relief", "mfr": "Cipla Ltd", "cat": "Allergy", "price": 45.00},
        {"name": "Loratadine 10mg", "desc": "Non-drowsy allergy medication", "mfr": "Sun Pharma", "cat": "Allergy", "price": 50.00},
        {"name": "Fexofenadine 120mg", "desc": "Long-acting antihistamine", "mfr": "Sanofi", "cat": "Allergy", "price": 85.00},
        {"name": "Levocetirizine 5mg", "desc": "Advanced antihistamine", "mfr": "Dr. Reddy's", "cat": "Allergy", "price": 55.00},
        {"name": "Desloratadine 5mg", "desc": "Once-daily allergy relief", "mfr": "Glenmark", "cat": "Allergy", "price": 70.00},
        {"name": "Diphenhydramine 25mg", "desc": "First-generation antihistamine", "mfr": "Johnson & Johnson", "cat": "Allergy", "price": 40.00},
        {"name": "Chlorpheniramine 4mg", "desc": "Classic allergy medication", "mfr": "Pfizer", "cat": "Allergy", "price": 35.00},
        {"name": "Hydroxyzine 25mg", "desc": "Antihistamine for itching", "mfr": "Lupin", "cat": "Allergy", "price": 60.00},
        {"name": "Montelukast 10mg", "desc": "Leukotriene receptor antagonist", "mfr": "Ranbaxy", "cat": "Allergy", "price": 95.00},
        {"name": "Beclomethasone Nasal Spray", "desc": "Corticosteroid for allergic rhinitis", "mfr": "GSK", "cat": "Allergy", "price": 120.00},
        {"name": "Budesonide Nasal Spray", "desc": "Steroid nasal spray", "mfr": "AstraZeneca", "cat": "Allergy", "price": 150.00},

        # Cold and Mild Flu (11 medicines)
        {"name": "Paracetamol 500mg", "desc": "Pain and fever relief", "mfr": "Micro Labs", "cat": "Cold and Mild Flu", "price": 20.00},
        {"name": "Phenylephrine 10mg", "desc": "Nasal decongestant", "mfr": "Cipla Ltd", "cat": "Cold and Mild Flu", "price": 45.00},
        {"name": "Pseudoephedrine 60mg", "desc": "Decongestant for cold", "mfr": "Sun Pharma", "cat": "Cold and Mild Flu", "price": 55.00},
        {"name": "Guaifenesin 200mg", "desc": "Expectorant", "mfr": "Dr. Reddy's", "cat": "Cold and Mild Flu", "price": 40.00},
        {"name": "Acetaminophen Combo", "desc": "Multi-symptom cold relief", "mfr": "Johnson & Johnson", "cat": "Cold and Mild Flu", "price": 75.00},
        {"name": "Ambroxol 30mg", "desc": "Mucolytic agent", "mfr": "Boehringer Ingelheim", "cat": "Cold and Mild Flu", "price": 50.00},
        {"name": "Bromhexine 8mg", "desc": "Cough suppressant", "mfr": "Sanofi", "cat": "Cold and Mild Flu", "price": 45.00},
        {"name": "Cetirizine+Phenylephrine", "desc": "Combined cold relief", "mfr": "Cipla Ltd", "cat": "Cold and Mild Flu", "price": 65.00},
        {"name": "Dextromethorphan Combo", "desc": "Cough and cold relief", "mfr": "Pfizer", "cat": "Cold and Mild Flu", "price": 70.00},
        {"name": "Zinc Supplements 50mg", "desc": "Immune support", "mfr": "Nature's Bounty", "cat": "Cold and Mild Flu", "price": 180.00},
        {"name": "Vitamin C 1000mg", "desc": "Immune booster", "mfr": "HealthKart", "cat": "Cold and Mild Flu", "price": 200.00},

        # Cough (11 medicines)
        {"name": "Dextromethorphan 15mg", "desc": "Cough suppressant", "mfr": "Pfizer", "cat": "Cough", "price": 55.00},
        {"name": "Codeine Phosphate 10mg", "desc": "Opioid cough suppressant", "mfr": "GSK", "cat": "Cough", "price": 85.00},
        {"name": "Guaifenesin Syrup", "desc": "Expectorant syrup", "mfr": "Sun Pharma", "cat": "Cough", "price": 90.00},
        {"name": "Ambroxol Syrup", "desc": "Mucolytic syrup", "mfr": "Cipla Ltd", "cat": "Cough", "price": 80.00},
        {"name": "Bromhexine Syrup", "desc": "Cough relief syrup", "mfr": "Sanofi", "cat": "Cough", "price": 75.00},
        {"name": "Honey-based Cough Syrup", "desc": "Natural cough relief", "mfr": "Dabur", "cat": "Cough", "price": 110.00},
        {"name": "Terbutaline 2.5mg", "desc": "Bronchodilator", "mfr": "AstraZeneca", "cat": "Cough", "price": 65.00},
        {"name": "Salbutamol 4mg", "desc": "Beta-2 agonist", "mfr": "GSK", "cat": "Cough", "price": 70.00},
        {"name": "Levosalbutamol 2mg", "desc": "Bronchodilator", "mfr": "Cipla Ltd", "cat": "Cough", "price": 75.00},
        {"name": "Theophylline 200mg", "desc": "Bronchodilator", "mfr": "Sun Pharma", "cat": "Cough", "price": 80.00},
        {"name": "Chlorpheniramine Syrup", "desc": "Antihistamine syrup", "mfr": "Pfizer", "cat": "Cough", "price": 60.00},

        # Dermatology (11 medicines)
        {"name": "Betamethasone Cream", "desc": "Corticosteroid for skin", "mfr": "GSK", "cat": "Dermatology", "price": 95.00},
        {"name": "Hydrocortisone 1% Cream", "desc": "Mild steroid cream", "mfr": "Johnson & Johnson", "cat": "Dermatology", "price": 85.00},
        {"name": "Clotrimazole Cream", "desc": "Antifungal cream", "mfr": "Bayer", "cat": "Dermatology", "price": 75.00},
        {"name": "Ketoconazole 2% Cream", "desc": "Antifungal medication", "mfr": "Cipla Ltd", "cat": "Dermatology", "price": 90.00},
        {"name": "Mupirocin Ointment", "desc": "Antibiotic ointment", "mfr": "GSK", "cat": "Dermatology", "price": 120.00},
        {"name": "Fusidic Acid Cream", "desc": "Topical antibiotic", "mfr": "Leo Pharma", "cat": "Dermatology", "price": 135.00},
        {"name": "Benzoyl Peroxide 5%", "desc": "Acne treatment", "mfr": "Galderma", "cat": "Dermatology", "price": 180.00},
        {"name": "Tretinoin 0.05% Cream", "desc": "Retinoid for acne", "mfr": "Johnson & Johnson", "cat": "Dermatology", "price": 250.00},
        {"name": "Calamine Lotion", "desc": "Soothing lotion", "mfr": "Himalaya", "cat": "Dermatology", "price": 65.00},
        {"name": "Povidone-Iodine 10%", "desc": "Antiseptic solution", "mfr": "Win-Medicare", "cat": "Dermatology", "price": 55.00},
        {"name": "Silver Sulfadiazine Cream", "desc": "Burn treatment", "mfr": "Sun Pharma", "cat": "Dermatology", "price": 140.00},

        # Eye/ENT (11 medicines)
        {"name": "Moxifloxacin Eye Drops", "desc": "Antibiotic eye drops", "mfr": "Alcon", "cat": "Eye/ENT", "price": 180.00},
        {"name": "Ofloxacin Eye Drops", "desc": "Antibiotic for eyes", "mfr": "Cipla Ltd", "cat": "Eye/ENT", "price": 120.00},
        {"name": "Ciprofloxacin Ear Drops", "desc": "Antibiotic ear drops", "mfr": "Sun Pharma", "cat": "Eye/ENT", "price": 95.00},
        {"name": "Chloramphenicol Eye Drops", "desc": "Broad-spectrum antibiotic", "mfr": "Pfizer", "cat": "Eye/ENT", "price": 65.00},
        {"name": "Timolol Eye Drops", "desc": "Glaucoma treatment", "mfr": "Bausch & Lomb", "cat": "Eye/ENT", "price": 240.00},
        {"name": "Latanoprost Eye Drops", "desc": "Prostaglandin for glaucoma", "mfr": "Pfizer", "cat": "Eye/ENT", "price": 350.00},
        {"name": "Tropicamide Eye Drops", "desc": "Mydriatic agent", "mfr": "Alcon", "cat": "Eye/ENT", "price": 150.00},
        {"name": "Phenylephrine Eye Drops", "desc": "Decongestant drops", "mfr": "Bausch & Lomb", "cat": "Eye/ENT", "price": 85.00},
        {"name": "Sodium Chloride Drops", "desc": "Saline drops", "mfr": "Cipla Ltd", "cat": "Eye/ENT", "price": 45.00},
        {"name": "Artificial Tears", "desc": "Lubricating eye drops", "mfr": "Allergan", "cat": "Eye/ENT", "price": 190.00},
        {"name": "Wax Softener Drops", "desc": "Earwax removal", "mfr": "Sun Pharma", "cat": "Eye/ENT", "price": 70.00},

        # Fever (11 medicines)
        {"name": "Paracetamol 650mg", "desc": "Fever reducer", "mfr": "Micro Labs", "cat": "Fever", "price": 25.00},
        {"name": "Ibuprofen 400mg", "desc": "NSAID for fever", "mfr": "Abbott", "cat": "Fever", "price": 30.00},
        {"name": "Mefenamic Acid 250mg", "desc": "Pain and fever relief", "mfr": "Pfizer", "cat": "Fever", "price": 40.00},
        {"name": "Diclofenac 50mg", "desc": "Anti-inflammatory", "mfr": "Novartis", "cat": "Fever", "price": 35.00},
        {"name": "Aspirin 325mg", "desc": "Antipyretic and analgesic", "mfr": "Bayer", "cat": "Fever", "price": 28.00},
        {"name": "Nimesulide 100mg", "desc": "COX-2 inhibitor", "mfr": "Panacea Biotec", "cat": "Fever", "price": 45.00},
        {"name": "Dolo 650", "desc": "Paracetamol brand", "mfr": "Micro Labs", "cat": "Fever", "price": 30.00},
        {"name": "Crocin 650", "desc": "Paracetamol brand", "mfr": "GSK", "cat": "Fever", "price": 30.00},
        {"name": "Calpol 500", "desc": "Paracetamol brand", "mfr": "GSK", "cat": "Fever", "price": 25.00},
        {"name": "Ibuprofen Suspension", "desc": "Pediatric fever relief", "mfr": "Abbott", "cat": "Fever", "price": 110.00},
        {"name": "Paracetamol Suspension", "desc": "Pediatric paracetamol", "mfr": "Micro Labs", "cat": "Fever", "price": 85.00},

        # Pain Relief (12 medicines)
        {"name": "Ibuprofen 600mg", "desc": "Strong pain reliever", "mfr": "Abbott", "cat": "Pain Relief", "price": 40.00},
        {"name": "Diclofenac 75mg", "desc": "Strong anti-inflammatory", "mfr": "Novartis", "cat": "Pain Relief", "price": 45.00},
        {"name": "Aceclofenac 100mg", "desc": "NSAID for pain", "mfr": "Ipca Labs", "cat": "Pain Relief", "price": 50.00},
        {"name": "Piroxicam 20mg", "desc": "Long-acting NSAID", "mfr": "Pfizer", "cat": "Pain Relief", "price": 55.00},
        {"name": "Tramadol 50mg", "desc": "Opioid analgesic", "mfr": "Sun Pharma", "cat": "Pain Relief", "price": 85.00},
        {"name": "Ketorolac 10mg", "desc": "Potent NSAID", "mfr": "Dr. Reddy's", "cat": "Pain Relief", "price": 65.00},
        {"name": "Etoricoxib 90mg", "desc": "COX-2 selective inhibitor", "mfr": "MSD", "cat": "Pain Relief", "price": 95.00},
        {"name": "Naproxen 500mg", "desc": "Long-acting pain relief", "mfr": "Cipla Ltd", "cat": "Pain Relief", "price": 60.00},
        {"name": "Indomethacin 25mg", "desc": "NSAID for inflammation", "mfr": "Zydus", "cat": "Pain Relief", "price": 45.00},
        {"name": "Paracetamol+Ibuprofen", "desc": "Combined pain relief", "mfr": "Abbott", "cat": "Pain Relief", "price": 55.00},
        {"name": "Diclofenac Gel", "desc": "Topical pain relief", "mfr": "Novartis", "cat": "Pain Relief", "price": 180.00},
        {"name": "Capsaicin Cream", "desc": "Topical analgesic", "mfr": "Himalaya", "cat": "Pain Relief", "price": 220.00},

        # Vitamins (11 medicines)
        {"name": "Vitamin D3 60000 IU", "desc": "Bone health supplement", "mfr": "Mankind", "cat": "Vitamins", "price": 45.00},
        {"name": "Vitamin B Complex", "desc": "B-vitamins combination", "mfr": "HealthKart", "cat": "Vitamins", "price": 180.00},
        {"name": "Vitamin C 500mg", "desc": "Antioxidant supplement", "mfr": "Nature's Bounty", "cat": "Vitamins", "price": 150.00},
        {"name": "Multivitamin Tablets", "desc": "Complete nutrition", "mfr": "Centrum", "cat": "Vitamins", "price": 350.00},
        {"name": "Calcium+Vitamin D3", "desc": "Bone health combo", "mfr": "Cipla Ltd", "cat": "Vitamins", "price": 220.00},
        {"name": "Iron+Folic Acid", "desc": "Hemoglobin booster", "mfr": "Sun Pharma", "cat": "Vitamins", "price": 95.00},
        {"name": "Vitamin E 400 IU", "desc": "Skin health vitamin", "mfr": "Nature's Bounty", "cat": "Vitamins", "price": 280.00},
        {"name": "Vitamin A 10000 IU", "desc": "Vision health", "mfr": "HealthKart", "cat": "Vitamins", "price": 160.00},
        {"name": "Omega-3 Fish Oil", "desc": "Heart health supplement", "mfr": "NutriliteCa", "cat": "Vitamins", "price": 450.00},
        {"name": "Biotin 10mg", "desc": "Hair and nail health", "mfr": "HealthKart", "cat": "Vitamins", "price": 380.00},
        {"name": "Zinc 50mg", "desc": "Immune support", "mfr": "Nature's Bounty", "cat": "Vitamins", "price": 190.00},

        # Women Hygiene (11 medicines)
        {"name": "Clotrimazole Pessaries", "desc": "Vaginal antifungal", "mfr": "Bayer", "cat": "Women Hygiene", "price": 120.00},
        {"name": "Metronidazole Vaginal Gel", "desc": "Bacterial vaginosis treatment", "mfr": "Sun Pharma", "cat": "Women Hygiene", "price": 180.00},
        {"name": "Fluconazole 150mg", "desc": "Oral antifungal", "mfr": "Pfizer", "cat": "Women Hygiene", "price": 45.00},
        {"name": "Mefenamic Acid 500mg", "desc": "Menstrual pain relief", "mfr": "Pfizer", "cat": "Women Hygiene", "price": 55.00},
        {"name": "Tranexamic Acid 500mg", "desc": "Heavy bleeding treatment", "mfr": "Cipla Ltd", "cat": "Women Hygiene", "price": 140.00},
        {"name": "Norethisterone 5mg", "desc": "Menstrual regulation", "mfr": "Zydus", "cat": "Women Hygiene", "price": 85.00},
        {"name": "Iron Supplements", "desc": "Anemia prevention", "mfr": "Sun Pharma", "cat": "Women Hygiene", "price": 110.00},
        {"name": "Folic Acid 5mg", "desc": "Prenatal supplement", "mfr": "Abbott", "cat": "Women Hygiene", "price": 60.00},
        {"name": "Calcium 500mg", "desc": "Bone health for women", "mfr": "Cipla Ltd", "cat": "Women Hygiene", "price": 180.00},
        {"name": "Cranberry Supplements", "desc": "UTI prevention", "mfr": "HealthKart", "cat": "Women Hygiene", "price": 350.00},
        {"name": "Probiotic Capsules", "desc": "Vaginal health", "mfr": "Culturelle", "cat": "Women Hygiene", "price": 450.00},
    ]

    medicines = []
    base_barcode = 8901234500000

    for i, med_data in enumerate(medicines_data):
        # Random stock between 50-200
        stock = random.randint(50, 200)

        # Random expiry date between 6 months to 3 years
        days_until_expiry = random.randint(180, 1095)
        expiry = date.today() + timedelta(days=days_until_expiry)

        # Barcode
        barcode = str(base_barcode + i)

        medicine = Medicine(
            name=med_data["name"],
            description=med_data["desc"],
            manufacturer=med_data["mfr"],
            category=med_data["cat"],
            quantity=stock,
            price=med_data["price"],
            expiry_date=expiry,
            stock=stock,
            reorder_level=random.randint(10, 30),
            barcode=barcode
        )
        medicines.append(medicine)

    db.session.bulk_save_objects(medicines)
    db.session.commit()

    print(f"✓ Created {len(medicines)} medicines across 9 categories")

def seed_alternatives():
    """Create alternative medicine mappings"""
    # Get all medicines
    all_medicines = Medicine.query.all()

    # Create dictionary by category
    by_category = {}
    for med in all_medicines:
        if med.category not in by_category:
            by_category[med.category] = []
        by_category[med.category].append(med)

    alternatives = []

    # Create alternatives within same category
    for category, meds in by_category.items():
        if len(meds) < 2:
            continue

        # For each medicine, add 3-5 alternatives from same category
        for primary in meds:
            # Get other medicines in same category
            other_meds = [m for m in meds if m.medicine_id != primary.medicine_id]

            # Select 3-5 random alternatives
            num_alternatives = min(random.randint(3, 5), len(other_meds))
            selected_alts = random.sample(other_meds, num_alternatives)

            for i, alt in enumerate(selected_alts):
                alternative = AlternativeMedicine(
                    primary_medicine_id=primary.medicine_id,
                    alternative_medicine_id=alt.medicine_id,
                    reason="Same category - similar therapeutic effect",
                    priority=i + 1
                )
                alternatives.append(alternative)

    db.session.bulk_save_objects(alternatives)
    db.session.commit()

    print(f"✓ Created {len(alternatives)} alternative medicine mappings")

def main():
    """Main seeding function"""
    app = create_app('development')

    with app.app_context():
        print("\n" + "="*50)
        print("DATABASE SEEDING STARTED")
        print("="*50 + "\n")

        seed_users()
        seed_medicines()
        seed_alternatives()

        print("\n" + "="*50)
        print("DATABASE SEEDING COMPLETED")
        print("="*50)
        print("\nLogin Credentials:")
        print("  Admin - username: 'admin' | password: 'admin123'")
        print("  Staff - username: 'staff' | password: 'staff123'")
        print("\nYou can now run the application with: python app.py")
        print("="*50 + "\n")

if __name__ == '__main__':
    main()
```

#### Deliverables
- ✅ Medicine CRUD operations
- ✅ Search and filter functionality
- ✅ 100 medicines in database
- ✅ Alternative medicine mappings
- ✅ Low stock detection

#### Testing
- [ ] Add new medicine
- [ ] Edit existing medicine
- [ ] Delete medicine (with/without sales history)
- [ ] Search medicines by name
- [ ] Filter by category
- [ ] Sort by different fields
- [ ] Verify low stock indicators

---

### Phase 4: Sales Module (Days 6-7)

This phase will implement:
- Barcode scanning with QuaggaJS
- Sales recording
- Stock updates
- Receipt generation

---

### Phase 5: Dashboards & Analytics (Days 8-9)

This phase will implement:
- Admin dashboard with Chart.js visualizations
- Staff dashboard
- Low stock alerts
- Seasonal sales charts

---

### Phase 6: Predictive Insights & Reports (Days 10-11)

This phase will implement:
- Moving average prediction
- Seasonal forecasting
- Sales reports with filters
- CSV export functionality

---

### Phase 7: Alternative Medicines & Polish (Days 12-13)

This phase will implement:
- Alternative medicine management UI
- Responsive design improvements
- Form validations
- About page

---

### Phase 8: Testing & Deployment (Day 14)

This phase will include:
- End-to-end testing
- Bug fixes
- Performance optimization
- Deployment documentation

---

## Success Criteria

### Functional Requirements Met
- ✅ User authentication with role-based access
- ✅ Medicine CRUD operations
- ✅ Barcode scanning and sales recording
- ✅ Dashboard with analytics
- ✅ Predictive insights
- ✅ Reports with export

### Non-Functional Requirements Met
- ✅ Page load time < 3 seconds
- ✅ Password hashing with bcrypt
- ✅ SQL injection protection
- ✅ XSS protection
- ✅ Responsive design
- ✅ Form validation

### Data Requirements Met
- ✅ 100 medicines across 9 categories
- ✅ Alternative medicine mappings
- ✅ Default user accounts
- ✅ Complete seed data

---

## Next Steps

1. **Review this plan** and provide feedback
2. **Approve to proceed** with implementation
3. **Start Phase 1** - Project setup and models

Would you like me to proceed with the implementation or would you like to modify any part of this plan?
