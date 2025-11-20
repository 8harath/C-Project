from flask import Blueprint, render_template
from flask_login import login_required
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard (placeholder for Phase 5)"""
    return render_template('admin/admin_dashboard.html')
