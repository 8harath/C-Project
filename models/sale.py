from datetime import datetime
from models import db

class Sale(db.Model):
    """Sale model for transaction recording"""

    __tablename__ = 'sale'

    sale_id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __init__(self, medicine_id, user_id, quantity_sold, total_price):
        self.medicine_id = medicine_id
        self.user_id = user_id
        self.quantity_sold = quantity_sold
        self.total_price = total_price

    @property
    def season(self):
        """Get season based on sale date"""
        month = self.sale_date.month
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Monsoon'

    def to_dict(self):
        """Convert sale to dictionary"""
        return {
            'sale_id': self.sale_id,
            'medicine_id': self.medicine_id,
            'medicine_name': self.medicine.name,
            'user_id': self.user_id,
            'seller_name': self.seller.username,
            'quantity_sold': self.quantity_sold,
            'total_price': float(self.total_price),
            'sale_date': self.sale_date.isoformat(),
            'season': self.season
        }

    def __repr__(self):
        return f'<Sale {self.sale_id}: {self.quantity_sold} units>'
