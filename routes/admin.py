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
    """Admin dashboard (placeholder for Phase 5)"""
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
