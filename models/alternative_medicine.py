from models import db

class AlternativeMedicine(db.Model):
    """Alternative medicine mapping model"""

    __tablename__ = 'alternative_medicine'

    alternative_id = db.Column(db.Integer, primary_key=True)
    primary_medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False, index=True)
    alternative_medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.medicine_id'), nullable=False)
    reason = db.Column(db.Text)
    priority = db.Column(db.Integer, default=5)

    __table_args__ = (
        db.UniqueConstraint('primary_medicine_id', 'alternative_medicine_id', name='unique_alternative'),
        db.CheckConstraint('priority >= 1 AND priority <= 10', name='check_priority_range'),
    )

    def __init__(self, primary_medicine_id, alternative_medicine_id, reason=None, priority=5):
        self.primary_medicine_id = primary_medicine_id
        self.alternative_medicine_id = alternative_medicine_id
        self.reason = reason
        self.priority = priority

    def __repr__(self):
        return f'<Alternative {self.primary_medicine_id} -> {self.alternative_medicine_id}>'
