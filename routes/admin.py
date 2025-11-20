from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db
from models.medicine import Medicine
from models.sale import Sale
from models.user import User
from routes.decorators import admin_required, staff_required
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from collections import defaultdict

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with analytics"""

    # Key metrics
    total_sales = db.session.query(func.sum(Sale.total_price)).scalar() or 0
    total_medicines = Medicine.query.count()
    low_stock_count = Medicine.query.filter(Medicine.stock <= Medicine.reorder_level).count()
    total_transactions = Sale.query.count()

    # Top selling medicines (pie chart data)
    top_selling = db.session.query(
        Medicine.name,
        func.sum(Sale.quantity_sold).label('total_quantity')
    ).join(Sale).group_by(Medicine.medicine_id).order_by(
        desc('total_quantity')
    ).limit(5).all()

    # Seasonal sales
    sales_data = Sale.query.all()
    seasonal_sales = defaultdict(float)
    for sale in sales_data:
        season = sale.get_season()
        seasonal_sales[season] += float(sale.total_price)

    # Low stock medicines
    low_stock_medicines = Medicine.query.filter(
        Medicine.stock <= Medicine.reorder_level
    ).order_by(Medicine.stock).all()

    return render_template('admin/admin_dashboard.html',
                           total_sales=total_sales,
                           total_medicines=total_medicines,
                           low_stock_count=low_stock_count,
                           total_transactions=total_transactions,
                           top_selling=top_selling,
                           seasonal_sales=seasonal_sales,
                           low_stock_medicines=low_stock_medicines)

@admin_bp.route('/staff/dashboard')
@staff_required
def staff_dashboard():
    """Staff dashboard with limited analytics"""

    # Low stock warning
    low_stock_count = Medicine.query.filter(Medicine.stock <= Medicine.reorder_level).count()
    low_stock_medicines = Medicine.query.filter(
        Medicine.stock <= Medicine.reorder_level
    ).order_by(Medicine.stock).limit(10).all()

    # Top selling medicines
    top_selling = db.session.query(
        Medicine.name,
        func.sum(Sale.quantity_sold).label('total_quantity')
    ).join(Sale).group_by(Medicine.medicine_id).order_by(
        desc('total_quantity')
    ).limit(10).all()

    return render_template('staff/staff_dashboard.html',
                           low_stock_count=low_stock_count,
                           low_stock_medicines=low_stock_medicines,
                           top_selling=top_selling)
