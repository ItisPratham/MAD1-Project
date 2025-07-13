from . import db
from datetime import datetime

class ReserveParkingSpot(db.Model):
    __tablename__ = "reserve_parking_spot"
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    cost_per_unit_time = db.Column(db.Float, nullable=False)
    vehicle_no = db.Column(db.String(10), nullable=False)

    @property
    def total_time(self):
        if not self.leaving_timestamp:
            return None
        return (self.leaving_timestamp - self.parking_timestamp).total_seconds()

    @property
    def total_cost(self):
        return round(self.total_time * self.cost_per_unit_time / 3600, 2)
    