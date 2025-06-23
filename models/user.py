from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    reservations = db.relationship('ReserveParkingSpot', backref='user')