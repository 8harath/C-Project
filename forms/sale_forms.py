from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length
from models.medicine import Medicine
from datetime import date

class SaleForm(FlaskForm):
    """Form for recording medicine sales"""
    medicine_id = SelectField('Medicine', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, message='Quantity must be at least 1')
    ])
    submit = SubmitField('Record Sale')

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        # Populate medicine choices with available medicines only
        self.medicine_id.choices = [(0, 'Select a medicine')] + [
            (m.medicine_id, f'{m.name} - {m.manufacturer} (Stock: {m.stock})')
            for m in Medicine.query.filter(Medicine.stock > 0, Medicine.expiry_date > date.today())
            .order_by(Medicine.name).all()
        ]

    def validate_medicine_id(self, field):
        """Validate that a medicine is selected"""
        if field.data == 0:
            raise ValidationError('Please select a medicine.')

        medicine = Medicine.query.get(field.data)
        if not medicine:
            raise ValidationError('Selected medicine not found.')

        # Check if medicine is expired
        if medicine.is_expired():
            raise ValidationError(f'{medicine.name} has expired and cannot be sold.')

    def validate_quantity(self, field):
        """Validate that sufficient stock is available"""
        if hasattr(self, 'medicine_id') and self.medicine_id.data:
            medicine = Medicine.query.get(self.medicine_id.data)
            if medicine and field.data > medicine.stock:
                raise ValidationError(
                    f'Insufficient stock. Only {medicine.stock} units available.'
                )


class BarcodeSaleForm(FlaskForm):
    """Form for recording sales via barcode scanning"""
    barcode = StringField('Barcode', validators=[
        DataRequired(),
        Length(min=13, max=13, message='Barcode must be exactly 13 digits')
    ])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, message='Quantity must be at least 1')
    ])
    submit = SubmitField('Record Sale')

    def validate_barcode(self, field):
        """Validate that medicine exists and is available"""
        medicine = Medicine.query.filter_by(barcode=field.data).first()
        if not medicine:
            raise ValidationError(f'No medicine found with barcode {field.data}.')

        # Check if medicine is expired
        if medicine.is_expired():
            raise ValidationError(f'{medicine.name} has expired and cannot be sold.')

        # Check stock availability
        if medicine.stock == 0:
            raise ValidationError(f'{medicine.name} is out of stock.')

    def validate_quantity(self, field):
        """Validate that sufficient stock is available"""
        if hasattr(self, 'barcode') and self.barcode.data:
            medicine = Medicine.query.filter_by(barcode=self.barcode.data).first()
            if medicine and field.data > medicine.stock:
                raise ValidationError(
                    f'Insufficient stock. Only {medicine.stock} units available.'
                )


class ManualBarcodeForm(FlaskForm):
    """Form for manual barcode entry"""
    barcode = StringField('Barcode', validators=[
        DataRequired(),
        Length(min=13, max=13, message='Barcode must be exactly 13 digits')
    ])
    submit = SubmitField('Lookup Medicine')

    def validate_barcode(self, field):
        """Validate barcode format"""
        if not field.data.isdigit():
            raise ValidationError('Barcode must contain only digits.')
