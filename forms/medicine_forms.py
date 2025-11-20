from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import date
from config import Config

class MedicineForm(FlaskForm):
    """Form for adding/editing medicines"""
    name = StringField('Medicine Name', validators=[
        DataRequired(message='Medicine name is required'),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[Length(max=500)])
    manufacturer = StringField('Manufacturer', validators=[
        DataRequired(message='Manufacturer is required'),
        Length(max=200)
    ])
    category = SelectField('Category', validators=[DataRequired()],
                          choices=[(cat, cat) for cat in Config.MEDICINE_CATEGORIES])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=0, message='Quantity cannot be negative')
    ])
    price = DecimalField('Price (₹)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Price cannot be negative')
    ], places=2)
    expiry_date = DateField('Expiry Date', validators=[DataRequired()], format='%Y-%m-%d')
    stock = IntegerField('Stock', validators=[
        DataRequired(),
        NumberRange(min=0, message='Stock cannot be negative')
    ])
    reorder_level = IntegerField('Reorder Level', validators=[
        DataRequired(),
        NumberRange(min=0, message='Reorder level cannot be negative')
    ], default=10)
    barcode = StringField('Barcode (13 digits)', validators=[
        DataRequired(),
        Length(min=13, max=13, message='Barcode must be exactly 13 digits')
    ])
    submit = SubmitField('Save Medicine')

    def validate_expiry_date(self, expiry_date):
        """Ensure expiry date is in the future"""
        if expiry_date.data <= date.today():
            raise ValidationError('Expiry date must be in the future')

    def validate_barcode(self, barcode):
        """Ensure barcode contains only digits"""
        if not barcode.data.isdigit():
            raise ValidationError('Barcode must contain only digits')

class SearchFilterForm(FlaskForm):
    """Form for searching and filtering medicines"""
    search = StringField('Search', validators=[Length(max=100)])
    category = SelectField('Category', choices=[('', 'All Categories')] +
                          [(cat, cat) for cat in Config.MEDICINE_CATEGORIES])
    sort_by = SelectField('Sort By', choices=[
        ('name', 'Name'),
        ('price', 'Price'),
        ('stock', 'Stock'),
        ('expiry_date', 'Expiry Date')
    ], default='name')
    submit = SubmitField('Filter')
