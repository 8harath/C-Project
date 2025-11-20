from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db
from models.medicine import Medicine, AlternativeMedicine
from models.sale import Sale
from routes.decorators import admin_required, staff_required
from datetime import datetime, date
from sqlalchemy import or_

medicine_bp = Blueprint('medicine', __name__)

@medicine_bp.route('/')
@login_required
def list_medicines():
    """View all medicines with search and filter"""

    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get search and filter parameters
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    sort_by = request.args.get('sort', 'name')

    # Build query
    query = Medicine.query

    # Apply search
    if search_query:
        query = query.filter(
            or_(
                Medicine.name.ilike(f'%{search_query}%'),
                Medicine.manufacturer.ilike(f'%{search_query}%'),
                Medicine.barcode.ilike(f'%{search_query}%')
            )
        )

    # Apply category filter
    if category_filter and category_filter in Medicine.CATEGORIES:
        query = query.filter(Medicine.category == category_filter)

    # Apply sorting
    if sort_by == 'name':
        query = query.order_by(Medicine.name)
    elif sort_by == 'price':
        query = query.order_by(Medicine.price)
    elif sort_by == 'stock':
        query = query.order_by(Medicine.stock)
    elif sort_by == 'expiry':
        query = query.order_by(Medicine.expiry_date)
    else:
        query = query.order_by(Medicine.name)

    # Paginate
    medicines = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('shared/medicines.html',
                           medicines=medicines,
                           categories=Medicine.CATEGORIES,
                           search_query=search_query,
                           category_filter=category_filter,
                           sort_by=sort_by)

@medicine_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_medicine():
    """Add new medicine (Admin only)"""

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        manufacturer = request.form.get('manufacturer', '').strip()
        category = request.form.get('category', '').strip()
        quantity = request.form.get('quantity', type=int)
        price = request.form.get('price', type=float)
        expiry_date_str = request.form.get('expiry_date', '').strip()
        stock = request.form.get('stock', type=int)
        reorder_level = request.form.get('reorder_level', type=int, default=10)
        barcode = request.form.get('barcode', '').strip()

        # Validation
        errors = []

        if not name or len(name) > 200:
            errors.append('Medicine name is required and must be less than 200 characters.')

        if not manufacturer or len(manufacturer) > 200:
            errors.append('Manufacturer is required and must be less than 200 characters.')

        if category not in Medicine.CATEGORIES:
            errors.append('Invalid category selected.')

        if quantity is None or quantity < 0:
            errors.append('Quantity must be a non-negative number.')

        if price is None or price < 0:
            errors.append('Price must be a non-negative number.')

        if stock is None or stock < 0:
            errors.append('Stock must be a non-negative number.')

        if not barcode or len(barcode) != 13 or not barcode.isdigit():
            errors.append('Barcode must be exactly 13 digits (EAN-13 format).')

        # Check barcode uniqueness
        if barcode and Medicine.query.filter_by(barcode=barcode).first():
            errors.append('Barcode already exists.')

        # Validate expiry date
        try:
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            if expiry_date <= date.today():
                errors.append('Expiry date must be in the future.')
        except ValueError:
            errors.append('Invalid expiry date format. Use YYYY-MM-DD.')
            expiry_date = None

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('admin/add_medicine.html', categories=Medicine.CATEGORIES)

        # Create medicine
        try:
            medicine = Medicine(
                name=name,
                description=description,
                manufacturer=manufacturer,
                category=category,
                quantity=quantity,
                price=price,
                expiry_date=expiry_date,
                stock=stock,
                reorder_level=reorder_level,
                barcode=barcode
            )
            db.session.add(medicine)
            db.session.commit()
            flash(f'Medicine "{name}" added successfully!', 'success')
            return redirect(url_for('medicine.list_medicines'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the medicine.', 'danger')
            return render_template('admin/add_medicine.html', categories=Medicine.CATEGORIES)

    return render_template('admin/add_medicine.html', categories=Medicine.CATEGORIES)

@medicine_bp.route('/edit/<int:medicine_id>', methods=['GET', 'POST'])
@admin_required
def edit_medicine(medicine_id):
    """Edit existing medicine (Admin only)"""

    medicine = Medicine.query.get_or_404(medicine_id)

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        manufacturer = request.form.get('manufacturer', '').strip()
        category = request.form.get('category', '').strip()
        quantity = request.form.get('quantity', type=int)
        price = request.form.get('price', type=float)
        expiry_date_str = request.form.get('expiry_date', '').strip()
        stock = request.form.get('stock', type=int)
        reorder_level = request.form.get('reorder_level', type=int)
        barcode = request.form.get('barcode', '').strip()

        # Validation (similar to add_medicine)
        errors = []

        if not name or len(name) > 200:
            errors.append('Medicine name is required and must be less than 200 characters.')

        if not manufacturer or len(manufacturer) > 200:
            errors.append('Manufacturer is required and must be less than 200 characters.')

        if category not in Medicine.CATEGORIES:
            errors.append('Invalid category selected.')

        if quantity is None or quantity < 0:
            errors.append('Quantity must be a non-negative number.')

        if price is None or price < 0:
            errors.append('Price must be a non-negative number.')

        if stock is None or stock < 0:
            errors.append('Stock must be a non-negative number.')

        if not barcode or len(barcode) != 13 or not barcode.isdigit():
            errors.append('Barcode must be exactly 13 digits.')

        # Check barcode uniqueness (excluding current medicine)
        existing = Medicine.query.filter(
            Medicine.barcode == barcode,
            Medicine.medicine_id != medicine_id
        ).first()
        if existing:
            errors.append('Barcode already exists.')

        # Validate expiry date
        try:
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            if expiry_date <= date.today():
                errors.append('Expiry date must be in the future.')
        except ValueError:
            errors.append('Invalid expiry date format.')
            expiry_date = None

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('admin/edit_medicine.html', medicine=medicine, categories=Medicine.CATEGORIES)

        # Update medicine
        try:
            medicine.name = name
            medicine.description = description
            medicine.manufacturer = manufacturer
            medicine.category = category
            medicine.quantity = quantity
            medicine.price = price
            medicine.expiry_date = expiry_date
            medicine.stock = stock
            medicine.reorder_level = reorder_level
            medicine.barcode = barcode
            medicine.updated_at = datetime.utcnow()

            db.session.commit()
            flash(f'Medicine "{name}" updated successfully!', 'success')
            return redirect(url_for('medicine.list_medicines'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the medicine.', 'danger')
            return render_template('admin/edit_medicine.html', medicine=medicine, categories=Medicine.CATEGORIES)

    return render_template('admin/edit_medicine.html', medicine=medicine, categories=Medicine.CATEGORIES)

@medicine_bp.route('/delete/<int:medicine_id>', methods=['POST'])
@admin_required
def delete_medicine(medicine_id):
    """Delete medicine (Admin only)"""

    medicine = Medicine.query.get_or_404(medicine_id)

    # Check if medicine has sales history
    has_sales = Sale.query.filter_by(medicine_id=medicine_id).first() is not None

    if has_sales:
        flash('Cannot delete medicine with sales history.', 'warning')
        return redirect(url_for('medicine.list_medicines'))

    try:
        db.session.delete(medicine)
        db.session.commit()
        flash(f'Medicine "{medicine.name}" deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the medicine.', 'danger')

    return redirect(url_for('medicine.list_medicines'))

@medicine_bp.route('/api/barcode/<barcode>')
@login_required
def get_medicine_by_barcode(barcode):
    """API endpoint to get medicine by barcode"""

    medicine = Medicine.query.filter_by(barcode=barcode).first()

    if not medicine:
        return jsonify({'error': 'Medicine not found'}), 404

    return jsonify({
        'medicine_id': medicine.medicine_id,
        'name': medicine.name,
        'manufacturer': medicine.manufacturer,
        'category': medicine.category,
        'price': float(medicine.price),
        'stock': medicine.stock,
        'expiry_date': medicine.expiry_date.isoformat(),
        'is_expired': medicine.is_expired(),
        'barcode': medicine.barcode
    })
