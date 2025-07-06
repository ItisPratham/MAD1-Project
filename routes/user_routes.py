from flask import render_template, redirect, url_for, session, Blueprint, request
from models import User, ReserveParkingSpot, ParkingLot, db
from datetime import datetime

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user-dashboard')
def user_dashboard():
    if session.get('username') and session.get('role') == 'user':
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            return render_template('error.html', message='User does not exist.', retry_url=url_for('auth_routes.user_login'))
        history = ReserveParkingSpot.query.filter(ReserveParkingSpot.user_id == user.id, ReserveParkingSpot.leaving_timestamp != None).order_by(ReserveParkingSpot.id.desc()).limit(5).all()
        current = ReserveParkingSpot.query.filter(ReserveParkingSpot.user_id == user.id, ReserveParkingSpot.leaving_timestamp == None).all()
        address = request.args.get('Address')
        lots = []
        if address:
            address = '%'+address+'%'
            lots = ParkingLot.query.filter(ParkingLot.address.ilike(address)).all()
        return render_template('user_dashboard.html', user=user, history=history, current=current, lots=lots)
    return redirect(url_for('auth_routes.user_login'))

@user_routes.route('/user-view-parking-history')
def view_history():
    if session.get('username') and session.get('role') == 'user':
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            return render_template('error.html', message='User does not exist.', retry_url=url_for('auth_routes.user_login'))
        history = ReserveParkingSpot.query.filter(ReserveParkingSpot.user_id == user.id, ReserveParkingSpot.leaving_timestamp != None).order_by(ReserveParkingSpot.id.desc()).all()
        return render_template('user_view_history.html', user=user, history=history)
    return redirect(url_for('auth_routes.user_login'))

@user_routes.route('/user-edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if session.get('username') and session.get('role') == 'user':
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            return render_template('error.html', message='User does not exist.', retry_url=url_for('auth_routes.user_login'))
        if request.method == 'POST':
            user.name = request.form['Name']
            user.username = request.form['Username']
            user.password = request.form['Password']
            db.session.commit()
            session['username'] = request.form['Username']
            return redirect(url_for('user_routes.user_dashboard'))
        return render_template('user_edit_profile.html', user=user)
    return redirect(url_for('auth_routes.user_login'))

@user_routes.route('/user-view-edit-spot/<int:reservation_id>', methods=['GET', 'POST'])
def edit_spot(reservation_id):
    if session.get('username') and session.get('role') == 'user':
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            return render_template('error.html', message='User does not exist.', retry_url=url_for('auth_routes.user_login'))
        reservation = ReserveParkingSpot.query.get_or_404(reservation_id)
        if request.method == 'POST' and not reservation.leaving_timestamp:
            reservation.leaving_timestamp = datetime.now()
            reservation.spot.status = 'A'
            db.session.commit()
            return redirect(url_for('user_routes.user_dashboard'))
        return render_template('user_edit_spot.html', user=user, reservation=reservation)
    return redirect(url_for('auth_routes.user_login'))

@user_routes.route('/user-book-spot/<int:lot_id>', methods=['GET', 'POST'])
def book_spot(lot_id):
    if session.get('username') and session.get('role') == 'user':
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            return render_template('error.html', message='User does not exist.', retry_url=url_for('auth_routes.user_login'))
        lot = ParkingLot.query.get_or_404(lot_id)
        available_spots = [s for s in lot.spots if s.status == 'A']
        if not available_spots:
            return render_template('error.html', message='No Available Spots, Try another parking lot', retry_url=url_for('auth_routes.user_dashboard'))
        spot = available_spots[0]
        if request.method == 'POST':
            vehicle_number = request.form.get('vehicle_number')
            reservation = ReserveParkingSpot(spot_id=spot.id, user_id=user.id, parking_timestamp=datetime.now(), cost_per_unit_time=lot.price, vehicle_no=vehicle_number)
            spot.status = 'O'
            db.session.add(reservation)
            db.session.commit()
            return redirect(url_for('user_routes.user_dashboard'))
        return render_template('user_book_spot.html', user=user, spot=spot)
    return redirect(url_for('auth_routes.user_login'))

@user_routes.route('/user-charts')
def charts():
    if session.get('username') and session.get('role') == 'user':
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            return render_template('error.html', message='User does not exist.', retry_url=url_for('auth_routes.user_login'))
        lots = ParkingLot.query.all()
        summary_data = []
        for lot in lots:
            cost = 0.0
            time = 0
            count = 0
            for spot in lot.spots:
                for reservation in spot.reservations:
                    if reservation.user_id == user.id:
                        cost += reservation.total_cost or 0
                        time += reservation.total_time
                        count += 1
            if count != 0:
                summary_data.append({'lot_name': lot.name, 'time': time, 'cost':  cost, 'count': count})
        return render_template('user_charts.html', summary_data=summary_data, user=user)
    return redirect(url_for('auth_routes.user_login'))