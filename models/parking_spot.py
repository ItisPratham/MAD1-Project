from . import db

class ParkingSpot(db.Model):
    __tablename__ = "parking_spot"
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), default='A', nullable=False)
    reservations = db.relationship('ReserveParkingSpot', backref = 'spot')