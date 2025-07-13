from . import db

class ParkingLot(db.Model):
    __tablename__ = "parking_lot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    spots_count = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot')

    @property
    def available(self):
        return sum(1 for s in self.spots if s.status == 'A')

    @property
    def occupied(self):
        return sum(1 for s in self.spots if s.status == 'O')

    @property
    def inactive(self):
        return sum(1 for s in self.spots if s.status == 'I')
    
    