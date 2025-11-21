from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from models import db
from models.medicine import Medicine
from models.sale import Sale
from models.user import User
from routes.decorators import admin_required, staff_required
from sqlalchemy import func, desc, or_, and_
from datetime import datetime, timedelta
from collections import defaultdict
import csv
import io
from utils import analytics

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

    # Category-wise sales
    category_sales = db.session.query(
        Medicine.category,
        func.sum(Sale.total_price).label('total_sales')
    ).join(Sale).group_by(Medicine.category).order_by(
        desc('total_sales')
    ).all()

    # Monthly sales trend (last 6 months)
    six_months_ago = datetime.now() - timedelta(days=180)
    monthly_sales = db.session.query(
        func.strftime('%Y-%m', Sale.sale_date).label('month'),
        func.sum(Sale.total_price).label('total')
    ).filter(Sale.sale_date >= six_months_ago).group_by('month').order_by('month').all()

    # Recent transactions
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(10).all()

    # Stock statistics
    out_of_stock_count = Medicine.query.filter(Medicine.stock == 0).count()
    expiring_soon_count = Medicine.query.filter(
        Medicine.expiry_date <= (datetime.now().date() + timedelta(days=30))
    ).count()

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
                           category_sales=category_sales,
                           monthly_sales=monthly_sales,
                           recent_sales=recent_sales,
                           out_of_stock_count=out_of_stock_count,
                           expiring_soon_count=expiring_soon_count,
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

    # Today's sales (staff's own sales)
    today = datetime.now().date()
    my_today_sales = Sale.query.filter(
        Sale.user_id == current_user.user_id,
        func.date(Sale.sale_date) == today
    ).count()

    my_today_revenue = db.session.query(func.sum(Sale.total_price)).filter(
        Sale.user_id == current_user.user_id,
        func.date(Sale.sale_date) == today
    ).scalar() or 0

    # Total medicines available
    available_medicines = Medicine.query.filter(
        Medicine.stock > 0,
        Medicine.expiry_date > datetime.now().date()
    ).count()

    return render_template('staff/staff_dashboard.html',
                           low_stock_count=low_stock_count,
                           low_stock_medicines=low_stock_medicines,
                           top_selling=top_selling,
                           my_today_sales=my_today_sales,
                           my_today_revenue=my_today_revenue,
                           available_medicines=available_medicines)


@admin_bp.route('/predictive-insights')
@admin_required
def predictive_insights():
    """Predictive insights page with forecasting and predictions"""

    # Get seasonal trends
    seasonal_data = analytics.get_seasonal_trends()

    # Get category trends
    category_trends = analytics.get_category_trends()

    # Get sales forecast
    forecast_data = analytics.generate_forecast_data(months_ahead=3)

    # Get stock predictions (medicines that will run out soon)
    stock_predictions = analytics.get_stock_predictions()

    # Get reorder recommendations
    reorder_recommendations = analytics.get_reorder_recommendations()

    # Get top medicines by revenue
    top_medicines = analytics.get_top_medicines_by_revenue(limit=10)

    # Get monthly sales data for trend visualization
    monthly_sales = analytics.get_monthly_sales_data(months=12)

    return render_template('admin/predictive_insights.html',
                           seasonal_data=seasonal_data,
                           category_trends=category_trends,
                           forecast_data=forecast_data,
                           stock_predictions=stock_predictions,
                           reorder_recommendations=reorder_recommendations,
                           top_medicines=top_medicines,
                           monthly_sales=monthly_sales)


@admin_bp.route('/reports')
@admin_required
def reports():
    """Sales reports with filtering and export options"""

    # Get filter parameters
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    category = request.args.get('category', '')
    medicine_id = request.args.get('medicine_id', '')
    user_id = request.args.get('user_id', '')

    # Base query
    query = db.session.query(
        Sale.sale_id,
        Sale.sale_date,
        Medicine.name.label('medicine_name'),
        Medicine.category,
        Sale.quantity_sold,
        Sale.total_price,
        User.username.label('seller_name')
    ).join(Medicine).join(User)

    # Apply filters
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Sale.sale_date >= start_dt)
        except ValueError:
            flash('Invalid start date format', 'warning')

    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            # Add one day to include the end date
            end_dt = end_dt + timedelta(days=1)
            query = query.filter(Sale.sale_date < end_dt)
        except ValueError:
            flash('Invalid end date format', 'warning')

    if category:
        query = query.filter(Medicine.category == category)

    if medicine_id:
        try:
            query = query.filter(Sale.medicine_id == int(medicine_id))
        except ValueError:
            pass

    if user_id:
        try:
            query = query.filter(Sale.user_id == int(user_id))
        except ValueError:
            pass

    # Order by date descending
    query = query.order_by(Sale.sale_date.desc())

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 50
    sales_pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Calculate summary statistics
    summary_query = db.session.query(
        func.count(Sale.sale_id).label('total_transactions'),
        func.sum(Sale.quantity_sold).label('total_quantity'),
        func.sum(Sale.total_price).label('total_revenue'),
        func.avg(Sale.total_price).label('avg_transaction_value')
    ).join(Medicine).join(User)

    # Apply same filters to summary
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            summary_query = summary_query.filter(Sale.sale_date >= start_dt)
        except ValueError:
            pass

    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            summary_query = summary_query.filter(Sale.sale_date < end_dt)
        except ValueError:
            pass

    if category:
        summary_query = summary_query.filter(Medicine.category == category)

    if medicine_id:
        try:
            summary_query = summary_query.filter(Sale.medicine_id == int(medicine_id))
        except ValueError:
            pass

    if user_id:
        try:
            summary_query = summary_query.filter(Sale.user_id == int(user_id))
        except ValueError:
            pass

    summary_result = summary_query.first()
    summary = {
        'total_transactions': summary_result.total_transactions or 0,
        'total_quantity': summary_result.total_quantity or 0,
        'total_revenue': float(summary_result.total_revenue or 0),
        'avg_transaction_value': float(summary_result.avg_transaction_value or 0)
    }

    # Get all categories for filter dropdown
    categories = db.session.query(Medicine.category).distinct().order_by(Medicine.category).all()
    categories = [cat[0] for cat in categories]

    # Get all medicines for filter dropdown
    medicines = Medicine.query.order_by(Medicine.name).all()

    # Get all users for filter dropdown
    users = User.query.order_by(User.username).all()

    return render_template('admin/reports.html',
                           sales=sales_pagination,
                           summary=summary,
                           categories=categories,
                           medicines=medicines,
                           users=users,
                           filters={
                               'start_date': start_date,
                               'end_date': end_date,
                               'category': category,
                               'medicine_id': medicine_id,
                               'user_id': user_id
                           })


@admin_bp.route('/reports/export')
@admin_required
def export_reports():
    """Export sales reports to CSV"""

    # Get filter parameters (same as reports route)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    category = request.args.get('category', '')
    medicine_id = request.args.get('medicine_id', '')
    user_id = request.args.get('user_id', '')

    # Base query
    query = db.session.query(
        Sale.sale_id,
        Sale.sale_date,
        Medicine.name.label('medicine_name'),
        Medicine.category,
        Medicine.manufacturer,
        Sale.quantity_sold,
        Medicine.price.label('unit_price'),
        Sale.total_price,
        User.username.label('seller_name')
    ).join(Medicine).join(User)

    # Apply filters (same logic as reports route)
    if start_date:
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Sale.sale_date >= start_dt)
        except ValueError:
            pass

    if end_date:
        try:
            end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Sale.sale_date < end_dt)
        except ValueError:
            pass

    if category:
        query = query.filter(Medicine.category == category)

    if medicine_id:
        try:
            query = query.filter(Sale.medicine_id == int(medicine_id))
        except ValueError:
            pass

    if user_id:
        try:
            query = query.filter(Sale.user_id == int(user_id))
        except ValueError:
            pass

    # Order by date
    query = query.order_by(Sale.sale_date.desc())

    # Get all results
    sales_data = query.all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow([
        'Sale ID',
        'Date',
        'Time',
        'Medicine Name',
        'Category',
        'Manufacturer',
        'Quantity Sold',
        'Unit Price',
        'Total Price',
        'Seller',
        'Season'
    ])

    # Write data rows
    for sale in sales_data:
        sale_obj = Sale.query.get(sale.sale_id)
        season = sale_obj.get_season() if sale_obj else 'N/A'

        writer.writerow([
            sale.sale_id,
            sale.sale_date.strftime('%Y-%m-%d'),
            sale.sale_date.strftime('%H:%M:%S'),
            sale.medicine_name,
            sale.category,
            sale.manufacturer,
            sale.quantity_sold,
            f'₹{float(sale.unit_price):.2f}',
            f'₹{float(sale.total_price):.2f}',
            sale.seller_name,
            season
        ])

    # Write summary at the end
    writer.writerow([])
    writer.writerow(['SUMMARY'])
    writer.writerow(['Total Transactions', len(sales_data)])
    writer.writerow(['Total Quantity Sold', sum(sale.quantity_sold for sale in sales_data)])
    writer.writerow(['Total Revenue', f'₹{sum(float(sale.total_price) for sale in sales_data):.2f}'])

    if len(sales_data) > 0:
        avg_transaction = sum(float(sale.total_price) for sale in sales_data) / len(sales_data)
        writer.writerow(['Average Transaction Value', f'₹{avg_transaction:.2f}'])

    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=sales_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response
