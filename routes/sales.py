from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import db
from models.medicine import Medicine, AlternativeMedicine
from models.sale import Sale
from forms.sale_forms import SaleForm, BarcodeSaleForm, ManualBarcodeForm
from routes.decorators import staff_required
from datetime import datetime, date
from decimal import Decimal

sales_bp = Blueprint('sales', __name__)

def get_available_alternatives(medicine):
    """Get list of available alternative medicines (in stock and not expired)"""
    alternatives = medicine.get_alternatives()
    available_alternatives = []

    for alt in alternatives:
        alt_medicine = Medicine.query.get(alt.alternative_medicine_id)
        if alt_medicine and alt_medicine.stock > 0 and not alt_medicine.is_expired():
            available_alternatives.append({
                'medicine': alt_medicine,
                'reason': alt.reason,
                'priority': alt.priority
            })

    return available_alternatives

@sales_bp.route('/sell', methods=['GET', 'POST'])
@login_required
@staff_required
def sell_medicines():
    """Sell medicines page with medicine selection"""

    form = SaleForm()

    if form.validate_on_submit():
        try:
            # Get medicine
            medicine = Medicine.query.get(form.medicine_id.data)

            if not medicine:
                flash('Medicine not found.', 'danger')
                return redirect(url_for('sales.sell_medicines'))

            # Validate stock
            if medicine.stock < form.quantity.data:
                flash(f'Insufficient stock. Only {medicine.stock} units available.', 'danger')

                # Suggest alternatives
                alternatives = get_available_alternatives(medicine)
                if alternatives:
                    alt_names = [alt['medicine'].name for alt in alternatives[:3]]
                    flash(f'Alternative medicines available: {", ".join(alt_names)}', 'info')

                return redirect(url_for('sales.sell_medicines'))

            # Validate expiry
            if medicine.is_expired():
                flash(f'{medicine.name} has expired and cannot be sold.', 'danger')

                # Suggest alternatives
                alternatives = get_available_alternatives(medicine)
                if alternatives:
                    alt_names = [alt['medicine'].name for alt in alternatives[:3]]
                    flash(f'Alternative medicines available: {", ".join(alt_names)}', 'info')

                return redirect(url_for('sales.sell_medicines'))

            # Calculate total price
            total_price = Decimal(str(medicine.price)) * Decimal(str(form.quantity.data))

            # Create sale record
            sale = Sale(
                medicine_id=medicine.medicine_id,
                user_id=current_user.user_id,
                quantity_sold=form.quantity.data,
                total_price=total_price
            )

            # Update stock
            medicine.stock -= form.quantity.data
            medicine.updated_at = datetime.utcnow()

            # Commit transaction
            db.session.add(sale)
            db.session.commit()

            flash(f'Sale recorded successfully! {form.quantity.data} units of {medicine.name} sold.', 'success')

            # Check for low stock warning
            if medicine.is_low_stock():
                flash(f'Warning: {medicine.name} is now low on stock ({medicine.stock} units remaining).', 'warning')

            return redirect(url_for('sales.receipt', sale_id=sale.sale_id))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred while recording the sale. Please try again.', 'danger')
            return redirect(url_for('sales.sell_medicines'))

    # Get available medicines for display
    medicines = Medicine.query.filter(
        Medicine.stock > 0,
        Medicine.expiry_date > date.today()
    ).order_by(Medicine.name).all()

    return render_template('shared/sell_medicines.html', form=form, medicines=medicines)


@sales_bp.route('/scan', methods=['GET'])
@login_required
@staff_required
def scan():
    """Barcode scanner page"""
    form = ManualBarcodeForm()
    return render_template('shared/scan.html', form=form)


@sales_bp.route('/sell/barcode', methods=['POST'])
@login_required
@staff_required
def sell_by_barcode():
    """Record sale via barcode"""

    # Get data from JSON request or form data
    if request.is_json:
        data = request.get_json()
        barcode = data.get('barcode', '').strip()
        quantity = data.get('quantity', 1)
    else:
        barcode = request.form.get('barcode', '').strip()
        quantity = request.form.get('quantity', 1, type=int)

    # Validate inputs
    if not barcode or len(barcode) != 13 or not barcode.isdigit():
        if request.is_json:
            return jsonify({'error': 'Invalid barcode format. Must be 13 digits.'}), 400
        flash('Invalid barcode format. Must be 13 digits.', 'danger')
        return redirect(url_for('sales.scan'))

    if quantity < 1:
        if request.is_json:
            return jsonify({'error': 'Quantity must be at least 1.'}), 400
        flash('Quantity must be at least 1.', 'danger')
        return redirect(url_for('sales.scan'))

    # Find medicine
    medicine = Medicine.query.filter_by(barcode=barcode).first()

    if not medicine:
        if request.is_json:
            return jsonify({'error': f'No medicine found with barcode {barcode}.'}), 404
        flash(f'No medicine found with barcode {barcode}.', 'danger')
        return redirect(url_for('sales.scan'))

    # Validate stock
    if medicine.stock < quantity:
        # Suggest alternatives
        alternatives = get_available_alternatives(medicine)
        alternative_info = []
        if alternatives:
            alternative_info = [{'name': alt['medicine'].name, 'id': alt['medicine'].medicine_id} for alt in alternatives[:3]]

        if request.is_json:
            response = {
                'error': f'Insufficient stock. Only {medicine.stock} units available.',
                'available_stock': medicine.stock
            }
            if alternative_info:
                response['alternatives'] = alternative_info
            return jsonify(response), 400

        flash(f'Insufficient stock. Only {medicine.stock} units available.', 'danger')
        if alternative_info:
            alt_names = [alt['name'] for alt in alternative_info]
            flash(f'Alternative medicines available: {", ".join(alt_names)}', 'info')
        return redirect(url_for('sales.scan'))

    # Validate expiry
    if medicine.is_expired():
        # Suggest alternatives
        alternatives = get_available_alternatives(medicine)
        alternative_info = []
        if alternatives:
            alternative_info = [{'name': alt['medicine'].name, 'id': alt['medicine'].medicine_id} for alt in alternatives[:3]]

        if request.is_json:
            response = {'error': f'{medicine.name} has expired and cannot be sold.'}
            if alternative_info:
                response['alternatives'] = alternative_info
            return jsonify(response), 400

        flash(f'{medicine.name} has expired and cannot be sold.', 'danger')
        if alternative_info:
            alt_names = [alt['name'] for alt in alternative_info]
            flash(f'Alternative medicines available: {", ".join(alt_names)}', 'info')
        return redirect(url_for('sales.scan'))

    try:
        # Calculate total price
        total_price = Decimal(str(medicine.price)) * Decimal(str(quantity))

        # Create sale record
        sale = Sale(
            medicine_id=medicine.medicine_id,
            user_id=current_user.user_id,
            quantity_sold=quantity,
            total_price=total_price
        )

        # Update stock
        medicine.stock -= quantity
        medicine.updated_at = datetime.utcnow()

        # Commit transaction
        db.session.add(sale)
        db.session.commit()

        # Prepare response
        low_stock = medicine.is_low_stock()

        if request.is_json:
            return jsonify({
                'success': True,
                'message': f'Sale recorded successfully! {quantity} units of {medicine.name} sold.',
                'sale_id': sale.sale_id,
                'low_stock': low_stock,
                'remaining_stock': medicine.stock,
                'receipt_url': url_for('sales.receipt', sale_id=sale.sale_id)
            }), 200

        flash(f'Sale recorded successfully! {quantity} units of {medicine.name} sold.', 'success')

        if low_stock:
            flash(f'Warning: {medicine.name} is now low on stock ({medicine.stock} units remaining).', 'warning')

        return redirect(url_for('sales.receipt', sale_id=sale.sale_id))

    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'error': 'An error occurred while recording the sale.'}), 500
        flash('An error occurred while recording the sale. Please try again.', 'danger')
        return redirect(url_for('sales.scan'))


@sales_bp.route('/receipt/<int:sale_id>')
@login_required
@staff_required
def receipt(sale_id):
    """View receipt for a sale"""

    sale = Sale.query.get_or_404(sale_id)

    # Get medicine and user details
    medicine = Medicine.query.get(sale.medicine_id)

    # Ensure user can only view their own receipts (unless admin)
    if current_user.role != 'Admin' and sale.user_id != current_user.user_id:
        flash('You do not have permission to view this receipt.', 'danger')
        return redirect(url_for('sales.sell_medicines'))

    return render_template('shared/receipt.html', sale=sale, medicine=medicine)


@sales_bp.route('/history')
@login_required
@staff_required
def sales_history():
    """View sales history"""

    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Staff can only see their own sales, Admin can see all
    if current_user.role == 'Admin':
        sales = Sale.query.order_by(Sale.sale_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        sales = Sale.query.filter_by(user_id=current_user.user_id).order_by(
            Sale.sale_date.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('shared/sales_history.html', sales=sales)
