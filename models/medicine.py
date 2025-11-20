from datetime import datetime
from models import db

class Medicine(db.Model):
    """Medicine model for inventory management"""

    __tablename__ = 'medicine'

    medicine_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    manufacturer = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False, index=True)
    stock = db.Column(db.Integer, nullable=False, default=0, index=True)
    reorder_level = db.Column(db.Integer, nullable=False, default=10)
    barcode = db.Column(db.String(13), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sales = db.relationship('Sale', backref='medicine', lazy='dynamic')
    alternatives_as_primary = db.relationship(
        'AlternativeMedicine',
        foreign_keys='AlternativeMedicine.primary_medicine_id',
        backref='primary_medicine',
        lazy='dynamic'
    )
    alternatives_as_alternative = db.relationship(
        'AlternativeMedicine',
        foreign_keys='AlternativeMedicine.alternative_medicine_id',
        backref='alternative_medicine',
        lazy='dynamic'
    )

    def __init__(self, name, manufacturer, category, quantity, price,
                 expiry_date, barcode, description=None, stock=None, reorder_level=10):
        self.name = name
        self.description = description
        self.manufacturer = manufacturer
        self.category = category
        self.quantity = quantity
        self.price = price
        self.expiry_date = expiry_date
        self.stock = stock if stock is not None else quantity
        self.reorder_level = reorder_level
        self.barcode = barcode

    def is_low_stock(self):
        """Check if medicine stock is below reorder level"""
        return self.stock <= self.reorder_level

    def is_expired(self):
        """Check if medicine is expired"""
        from datetime import date
        return self.expiry_date < date.today()

    def is_expiring_soon(self, days=30):
        """Check if medicine expires within specified days"""
        from datetime import date, timedelta
        return self.expiry_date <= (date.today() + timedelta(days=days))

    def update_stock(self, quantity_sold):
        """Update stock after sale"""
        if self.stock >= quantity_sold:
            self.stock -= quantity_sold
            return True
        return False

    def to_dict(self):
        """Convert medicine to dictionary (for API responses)"""
        return {
            'medicine_id': self.medicine_id,
            'name': self.name,
            'description': self.description,
            'manufacturer': self.manufacturer,
            'category': self.category,
            'quantity': self.quantity,
            'price': float(self.price),
            'expiry_date': self.expiry_date.isoformat(),
            'stock': self.stock,
            'reorder_level': self.reorder_level,
            'barcode': self.barcode,
            'is_low_stock': self.is_low_stock(),
            'is_expired': self.is_expired()
        }

    def __repr__(self):
        return f'<Medicine {self.name} (Stock: {self.stock})>'
