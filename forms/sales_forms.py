"""
Sales and barcode scanning forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError, Optional
from models.medicine import Medicine


class BarcodeScanForm(FlaskForm):
    """Form for barcode scanning interface"""
    barcode = StringField(
        'Barcode',
        validators=[
            DataRequired(message='Barcode is required'),
            Length(min=13, max=13, message='Barcode must be exactly 13 digits')
        ],
        render_kw={'placeholder': 'Scan or enter barcode', 'autofocus': True}
    )
    submit = SubmitField('Search Product')

    def validate_barcode(self, barcode):
        """Validate that barcode contains only digits"""
        if not barcode.data.isdigit():
            raise ValidationError('Barcode must contain only digits')


class SaleItemForm(FlaskForm):
    """Form for adding individual sale items"""
    medicine_id = HiddenField('Medicine ID', validators=[DataRequired()])
    medicine_name = StringField('Medicine Name', render_kw={'readonly': True})
    price = DecimalField('Price (₹)', places=2, render_kw={'readonly': True})
    available_stock = IntegerField('Available Stock', render_kw={'readonly': True})
    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired(message='Quantity is required'),
            NumberRange(min=1, message='Quantity must be at least 1')
        ],
        default=1,
        render_kw={'min': 1}
    )

    def validate_quantity(self, quantity):
        """Validate that requested quantity is available in stock"""
        if hasattr(self, 'medicine_id') and self.medicine_id.data:
            medicine = Medicine.query.get(int(self.medicine_id.data))
            if medicine:
                if quantity.data > medicine.stock:
                    raise ValidationError(f'Only {medicine.stock} units available in stock')
                if medicine.is_expired():
                    raise ValidationError('This medicine has expired and cannot be sold')


class CompleteSaleForm(FlaskForm):
    """Form for completing a sale transaction"""
    customer_name = StringField(
        'Customer Name',
        validators=[Optional(), Length(max=200)],
        render_kw={'placeholder': 'Optional'}
    )
    customer_phone = StringField(
        'Customer Phone',
        validators=[Optional(), Length(min=10, max=15)],
        render_kw={'placeholder': 'Optional'}
    )
    payment_method = StringField(
        'Payment Method',
        validators=[DataRequired(message='Payment method is required')],
        default='Cash'
    )
    submit = SubmitField('Complete Sale')


class QuickSaleForm(FlaskForm):
    """Form for quick sale by barcode"""
    barcode = StringField(
        'Barcode',
        validators=[
            DataRequired(message='Barcode is required'),
            Length(min=13, max=13, message='Barcode must be exactly 13 digits')
        ],
        render_kw={'placeholder': 'Scan barcode', 'autofocus': True}
    )
    quantity = IntegerField(
        'Quantity',
        validators=[
            DataRequired(message='Quantity is required'),
            NumberRange(min=1, message='Quantity must be at least 1')
        ],
        default=1,
        render_kw={'min': 1}
    )

    def validate_barcode(self, barcode):
        """Validate that barcode exists and medicine is available"""
        if not barcode.data.isdigit():
            raise ValidationError('Barcode must contain only digits')

        medicine = Medicine.query.filter_by(barcode=barcode.data).first()
        if not medicine:
            raise ValidationError('Medicine not found with this barcode')

        if medicine.is_expired():
            raise ValidationError('This medicine has expired and cannot be sold')

        if medicine.stock == 0:
            raise ValidationError('This medicine is out of stock')
