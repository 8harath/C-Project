from flask import Blueprint, render_template, request
from flask_login import login_required
from utils.decorators import staff_required
from models.medicine import Medicine
from forms.medicine_forms import SearchFilterForm
from sqlalchemy import or_

shared_bp = Blueprint('shared', __name__)

@shared_bp.route('/about')
def about():
    """About page"""
    return render_template('shared/about.html')

@shared_bp.route('/products')
@login_required
@staff_required
def products():
    """View all products (read-only for staff)"""
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

    return render_template('shared/products.html',
                          medicines=medicines,
                          form=form)

@shared_bp.route('/sell')
@login_required
@staff_required
def sell():
    """Sell medicines page (placeholder for Phase 4)"""
    return render_template('shared/sell_medicines.html')

@shared_bp.route('/scan')
@login_required
@staff_required
def scan():
    """Barcode scan page (placeholder for Phase 4)"""
    return render_template('shared/scan.html')
