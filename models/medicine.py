from datetime import datetime, date
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
    alternatives_primary = db.relationship(
        'AlternativeMedicine',
        foreign_keys='AlternativeMedicine.primary_medicine_id',
        backref='primary_medicine',
        lazy='dynamic'
    )
    alternatives_alternative = db.relationship(
        'AlternativeMedicine',
        foreign_keys='AlternativeMedicine.alternative_medicine_id',
        backref='alternative_medicine',
        lazy='dynamic'
    )

    # Valid categories
    CATEGORIES = [
        'Allergy',
        'Cold and Mild Flu',
        'Cough',
        'Dermatology',
        'Eye/ENT',
        'Fever',
        'Pain Relief',
        'Vitamins',
        'Women Hygiene'
    ]

    def __init__(self, **kwargs):
        super(Medicine, self).__init__(**kwargs)

    def is_low_stock(self):
        """Check if medicine stock is below reorder level"""
        return self.stock <= self.reorder_level

    def is_expired(self):
        """Check if medicine has expired"""
        return self.expiry_date < date.today()

    def is_expiring_soon(self, days=30):
        """Check if medicine is expiring within specified days"""
        from datetime import timedelta
        return self.expiry_date <= date.today() + timedelta(days=days)

    def get_alternatives(self):
        """Get list of alternative medicines"""
        return AlternativeMedicine.query.filter_by(
            primary_medicine_id=self.medicine_id
        ).order_by(AlternativeMedicine.priority.desc()).all()

    def __repr__(self):
        return f'<Medicine {self.name} - {self.barcode}>'


class AlternativeMedicine(db.Model):
    """Alternative medicine mapping model"""

    __tablename__ = 'alternative_medicine'

    alternative_id = db.Column(db.Integer, primary_key=True)
    primary_medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False)
    alternative_medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False)
    reason = db.Column(db.Text)
    priority = db.Column(db.Integer, default=5)

    # Unique constraint to prevent duplicate mappings
    __table_args__ = (
        db.UniqueConstraint('primary_medicine_id', 'alternative_medicine_id', name='unique_alternative'),
        db.CheckConstraint('priority >= 1 AND priority <= 10', name='check_priority_range'),
    )

    def __repr__(self):
        return f'<AlternativeMedicine primary={self.primary_medicine_id} alt={self.alternative_medicine_id}>'
