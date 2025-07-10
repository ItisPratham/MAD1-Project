from flask import render_template, redirect, url_for, session, Blueprint, request
from models import User, ReserveParkingSpot, ParkingLot, db
from datetime import datetime
from flask_login import login_required, current_user
import re

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user-dashboard')
@login_required
def user_dashboard():
    history = ReserveParkingSpot.query.filter(ReserveParkingSpot.user_id == current_user.id, ReserveParkingSpot.leaving_timestamp != None).order_by(ReserveParkingSpot.id.desc()).limit(5).all()
    current = ReserveParkingSpot.query.filter(ReserveParkingSpot.user_id == current_user.id, ReserveParkingSpot.leaving_timestamp == None).all()
    address = request.args.get('Address')
    lots = []
    if address:
        address = '%'+address+'%'
        lots = ParkingLot.query.filter(ParkingLot.address.ilike(address)).all()
    return render_template('user_dashboard.html', user=current_user, history=history, current=current, lots=lots)

@user_routes.route('/user-view-parking-history')
@login_required
def view_history():
    history = ReserveParkingSpot.query.filter(ReserveParkingSpot.user_id == current_user.id, ReserveParkingSpot.leaving_timestamp != None).order_by(ReserveParkingSpot.id.desc()).all()
    return render_template('user_view_history.html', user=current_user, history=history)


@user_routes.route('/user-edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        name = request.form['Name'].strip()
        username = request.form['Username'].strip().lower()
        password = request.form['Password']

        if not re.match(r'^[A-Za-z\s]{3,}$', name):
            return render_template('error.html', message="Invalid name. Name must have atleast 3 characters.", retry_url=url_for('auth_routes.user_registration'))
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username):
            return render_template('error.html', message="Invalid email format.", retry_url=url_for('auth_routes.user_registration'))
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,12}$', password):
            return render_template('error.html', message="Password must be 8-12 characters long with atleast 1 num, and 1 uppercase and 1 lowercase alphabet.", retry_url=url_for('auth_routes.user_registration'))

        current_user.name = name
        current_user.username = username
        current_user.set_password(password)
        db.session.commit()
        session['username'] = request.form['Username']
        return redirect(url_for('user_routes.user_dashboard'))
    return render_template('user_edit_profile.html', user=current_user)

@user_routes.route('/user-view-edit-spot/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
def edit_spot(reservation_id):
    reservation = ReserveParkingSpot.query.get_or_404(reservation_id)
    if request.method == 'POST' and not reservation.leaving_timestamp:
        reservation.leaving_timestamp = datetime.now()
        reservation.spot.status = 'A'
        db.session.commit()
        return redirect(url_for('user_routes.user_dashboard'))
    return render_template('user_edit_spot.html', user=current_user, reservation=reservation)

@user_routes.route('/user-book-spot/<int:lot_id>', methods=['GET', 'POST'])
@login_required
def book_spot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    available_spots = [s for s in lot.spots if s.status == 'A']
    if not available_spots:
        return render_template('error.html', message='No Available Spots, Try another parking lot', retry_url=url_for('auth_routes.user_dashboard'))
    spot = available_spots[0]
    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number').strip().upper()
        
        if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$', vehicle_number):
            return render_template('error.html', message="Enter valid vehicle no of format 'AB01CD2345'", retry_url=url_for('user_routes.user_dashboard'))

        reservation = ReserveParkingSpot(spot_id=spot.id, user_id=int(current_user.id), parking_timestamp=datetime.now(), cost_per_unit_time=lot.price, vehicle_no=vehicle_number)
        spot.status = 'O'
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for('user_routes.user_dashboard'))
    return render_template('user_book_spot.html', user=current_user, spot=spot)

@user_routes.route('/user-charts')
@login_required
def charts():
    lots = ParkingLot.query.all()
    summary_data = []
    for lot in lots:
        cost = 0.0
        time = 0
        count = 0
        for spot in lot.spots:
            for reservation in spot.reservations:
                if reservation.leaving_timestamp and reservation.user_id == current_user.id:
                    cost += reservation.total_cost
                    time += reservation.total_time
                    count += 1
        if count != 0:
            summary_data.append({'lot_name': lot.name, 'time': time, 'cost':  cost, 'count': count})
    return render_template('user_charts.html', summary_data=summary_data, user=current_user)