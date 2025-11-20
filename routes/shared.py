from flask import Blueprint, render_template
from flask_login import login_required
from utils.decorators import staff_required

shared_bp = Blueprint('shared', __name__)

@shared_bp.route('/about')
def about():
    """About page"""
    return render_template('shared/about.html')

@shared_bp.route('/products')
@login_required
@staff_required
def products():
    """View all products (placeholder for Phase 3)"""
    return render_template('shared/products.html')

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
