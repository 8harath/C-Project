from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import login_required, current_user
from utils.decorators import staff_required
from models import db
from models.medicine import Medicine
from models.sale import Sale
from forms.medicine_forms import SearchFilterForm
from forms.sales_forms import BarcodeScanForm, CompleteSaleForm, QuickSaleForm
from sqlalchemy import or_
from datetime import datetime
from decimal import Decimal

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

@shared_bp.route('/sell', methods=['GET', 'POST'])
@login_required
@staff_required
def sell():
    """Sell medicines page with cart functionality"""
    form = CompleteSaleForm()

    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = []

    # Handle sale completion
    if form.validate_on_submit():
        cart = session.get('cart', [])

        if not cart:
            flash('Cart is empty. Add items before completing sale.', 'warning')
            return redirect(url_for('shared.sell'))

        try:
            # Calculate total
            total_amount = sum(Decimal(str(item['subtotal'])) for item in cart)

            # Create separate sale record for each item in cart
            first_sale_id = None
            for item in cart:
                medicine = Medicine.query.get(item['medicine_id'])
                if not medicine:
                    flash(f"Medicine {item['name']} not found", 'danger')
                    db.session.rollback()
                    return redirect(url_for('shared.sell'))

                if not medicine.update_stock(item['quantity']):
                    flash(f"Insufficient stock for {medicine.name}. Available: {medicine.stock}", 'danger')
                    db.session.rollback()
                    return redirect(url_for('shared.sell'))

                # Create sale record for this item
                item_total = Decimal(str(item['price'])) * item['quantity']
                sale = Sale(
                    medicine_id=medicine.medicine_id,
                    user_id=current_user.user_id,
                    quantity_sold=item['quantity'],
                    total_price=item_total
                )
                db.session.add(sale)
                db.session.flush()  # Flush to get the sale_id

                if first_sale_id is None:
                    first_sale_id = sale.sale_id

            db.session.commit()

            # Store sale info for receipt
            session['last_sale'] = {
                'sale_id': first_sale_id,
                'total_amount': float(total_amount),
                'items': cart,
                'customer_name': form.customer_name.data,
                'payment_method': form.payment_method.data,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # Clear cart
            session['cart'] = []

            flash(f'Sale completed successfully! Total: ₹{total_amount:.2f}', 'success')
            return redirect(url_for('shared.receipt'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error completing sale: {str(e)}', 'danger')
            return redirect(url_for('shared.sell'))

    # Calculate cart total
    cart = session.get('cart', [])
    cart_total = sum(Decimal(str(item['subtotal'])) for item in cart)

    return render_template('shared/sell.html',
                          form=form,
                          cart=cart,
                          cart_total=cart_total)


@shared_bp.route('/add_to_cart', methods=['POST'])
@login_required
@staff_required
def add_to_cart():
    """Add item to cart via AJAX"""
    data = request.get_json()

    medicine_id = data.get('medicine_id')
    quantity = data.get('quantity', 1)

    try:
        quantity = int(quantity)
        if quantity < 1:
            return jsonify({'success': False, 'message': 'Quantity must be at least 1'}), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400

    medicine = Medicine.query.get(medicine_id)

    if not medicine:
        return jsonify({'success': False, 'message': 'Medicine not found'}), 404

    if medicine.is_expired():
        return jsonify({'success': False, 'message': 'This medicine has expired'}), 400

    if medicine.stock < quantity:
        return jsonify({
            'success': False,
            'message': f'Insufficient stock. Available: {medicine.stock} units'
        }), 400

    # Initialize cart
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    # Check if item already in cart
    for item in cart:
        if item['medicine_id'] == medicine_id:
            # Update quantity
            new_quantity = item['quantity'] + quantity
            if new_quantity > medicine.stock:
                return jsonify({
                    'success': False,
                    'message': f'Cannot add more. Max available: {medicine.stock} units'
                }), 400
            item['quantity'] = new_quantity
            item['subtotal'] = float(medicine.price) * new_quantity
            session.modified = True
            return jsonify({
                'success': True,
                'message': f'Updated {medicine.name} quantity to {new_quantity}',
                'cart_count': len(cart)
            })

    # Add new item to cart
    cart_item = {
        'medicine_id': medicine_id,
        'name': medicine.name,
        'price': float(medicine.price),
        'quantity': quantity,
        'subtotal': float(medicine.price) * quantity,
        'barcode': medicine.barcode
    }

    cart.append(cart_item)
    session['cart'] = cart
    session.modified = True

    return jsonify({
        'success': True,
        'message': f'Added {medicine.name} to cart',
        'cart_count': len(cart)
    })


@shared_bp.route('/remove_from_cart/<int:index>', methods=['POST'])
@login_required
@staff_required
def remove_from_cart(index):
    """Remove item from cart"""
    cart = session.get('cart', [])

    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        session['cart'] = cart
        session.modified = True
        flash(f'Removed {removed_item["name"]} from cart', 'info')
    else:
        flash('Invalid cart item', 'danger')

    return redirect(url_for('shared.sell'))


@shared_bp.route('/clear_cart', methods=['POST'])
@login_required
@staff_required
def clear_cart():
    """Clear entire cart"""
    session['cart'] = []
    session.modified = True
    flash('Cart cleared', 'info')
    return redirect(url_for('shared.sell'))


@shared_bp.route('/scan', methods=['GET', 'POST'])
@login_required
@staff_required
def scan():
    """Barcode scan page with QuaggaJS integration"""
    form = BarcodeScanForm()
    medicine = None

    if form.validate_on_submit():
        barcode = form.barcode.data
        medicine = Medicine.query.filter_by(barcode=barcode).first()

        if not medicine:
            flash(f'No medicine found with barcode: {barcode}', 'warning')
        elif medicine.is_expired():
            flash(f'{medicine.name} has expired and cannot be sold', 'danger')
        elif medicine.stock == 0:
            flash(f'{medicine.name} is out of stock', 'warning')
        else:
            flash(f'Found: {medicine.name}', 'success')

    return render_template('shared/scan.html',
                          form=form,
                          medicine=medicine)


@shared_bp.route('/api/scan_barcode', methods=['POST'])
@login_required
@staff_required
def api_scan_barcode():
    """API endpoint for barcode scanning via QuaggaJS"""
    data = request.get_json()
    barcode = data.get('barcode', '').strip()

    if not barcode:
        return jsonify({'success': False, 'message': 'No barcode provided'}), 400

    if len(barcode) != 13 or not barcode.isdigit():
        return jsonify({'success': False, 'message': 'Invalid barcode format'}), 400

    medicine = Medicine.query.filter_by(barcode=barcode).first()

    if not medicine:
        return jsonify({
            'success': False,
            'message': f'Medicine not found with barcode: {barcode}'
        }), 404

    if medicine.is_expired():
        return jsonify({
            'success': False,
            'message': f'{medicine.name} has expired',
            'medicine': {
                'id': medicine.medicine_id,
                'name': medicine.name,
                'price': float(medicine.price),
                'stock': medicine.stock,
                'expired': True
            }
        }), 400

    return jsonify({
        'success': True,
        'message': f'Found: {medicine.name}',
        'medicine': {
            'id': medicine.medicine_id,
            'name': medicine.name,
            'manufacturer': medicine.manufacturer,
            'category': medicine.category,
            'price': float(medicine.price),
            'stock': medicine.stock,
            'expiry_date': medicine.expiry_date.strftime('%Y-%m-%d'),
            'barcode': medicine.barcode,
            'is_low_stock': medicine.is_low_stock(),
            'is_expiring_soon': medicine.is_expiring_soon()
        }
    })


@shared_bp.route('/receipt')
@login_required
@staff_required
def receipt():
    """Display receipt for last sale"""
    sale_data = session.get('last_sale')

    if not sale_data:
        flash('No recent sale found', 'warning')
        return redirect(url_for('shared.sell'))

    return render_template('shared/receipt.html', sale=sale_data)


@shared_bp.route('/api/search_medicines', methods=['GET'])
@login_required
@staff_required
def api_search_medicines():
    """API endpoint for searching medicines"""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'medicines': []}), 200

    if len(query) < 2:
        return jsonify({'medicines': [], 'message': 'Query too short'}), 200

    # Search by name or manufacturer
    search_term = f"%{query}%"
    medicines = Medicine.query.filter(or_(
        Medicine.name.ilike(search_term),
        Medicine.manufacturer.ilike(search_term)
    )).limit(20).all()

    results = []
    for medicine in medicines:
        results.append({
            'id': medicine.medicine_id,
            'name': medicine.name,
            'manufacturer': medicine.manufacturer,
            'category': medicine.category,
            'price': float(medicine.price),
            'stock': medicine.stock,
            'barcode': medicine.barcode,
            'is_low_stock': medicine.is_low_stock(),
            'is_expired': medicine.is_expired(),
            'is_expiring_soon': medicine.is_expiring_soon()
        })

    return jsonify({'medicines': results})
