from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from models import db
from models.user import User
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('admin.staff_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        if not username or not password:
            flash('Please provide both username and password.', 'danger')
            return render_template('auth/login.html')

        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return render_template('auth/login.html')

        login_user(user, remember=remember)
        flash(f'Welcome back, {user.username}!', 'success')

        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if user.is_admin():
                next_page = url_for('admin.dashboard')
            else:
                next_page = url_for('admin.staff_dashboard')
        return redirect(next_page)

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'Staff')

        # Validation
        errors = []

        if not username or len(username) < 3 or len(username) > 20:
            errors.append('Username must be between 3 and 20 characters.')

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores.')

        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append('Please provide a valid email address.')

        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        if role not in ['Admin', 'Staff']:
            role = 'Staff'

        # Check for existing username or email
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists.')

        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')

        # Create new user
        try:
            user = User(username=username, email=email, password=password, role=role)
            db.session.add(user)
            db.session.commit()
            flash(f'Registration successful! Welcome, {username}. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
