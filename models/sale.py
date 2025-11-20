from datetime import datetime
from models import db

class Sale(db.Model):
    """Sale model for tracking medicine sales"""

    __tablename__ = 'sale'

    sale_id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Constraints
    __table_args__ = (
        db.CheckConstraint('quantity_sold > 0', name='check_quantity_sold_positive'),
        db.CheckConstraint('total_price >= 0', name='check_total_price_non_negative'),
    )

    def __init__(self, medicine_id, user_id, quantity_sold, total_price):
        self.medicine_id = medicine_id
        self.user_id = user_id
        self.quantity_sold = quantity_sold
        self.total_price = total_price

    def get_season(self):
        """Get the season for this sale based on sale_date"""
        month = self.sale_date.month
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:  # 9, 10, 11
            return 'Monsoon'

    @staticmethod
    def get_season_for_month(month):
        """Get season for a given month number"""
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:  # 9, 10, 11
            return 'Monsoon'

    def __repr__(self):
        return f'<Sale {self.sale_id}: Medicine {self.medicine_id} x{self.quantity_sold}>'
