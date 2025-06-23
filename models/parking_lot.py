from . import db

class ParkingLot(db.Model):
    __tablename__ = "parking_lot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200))
    pin_code = db.Column(db.Integer)
    spots_count = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot')