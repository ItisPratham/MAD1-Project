from flask import render_template, request, redirect, url_for, session, Blueprint
from models import db, User, ParkingLot, ParkingSpot, ReserveParkingSpot

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin-dashboard')
def admin_dashboard():
    if session.get('username') and session.get('role') == 'admin':
        parking_lots = ParkingLot.query.all()
        return render_template('admin_dashboard.html', parking_lots=parking_lots)
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-add-parking-lot', methods=['GET', 'POST'])
def add_lot():
    if session.get('username') and session.get('role') == 'admin':
        if request.method == 'POST':
            name = request.form['LotName']
            price = float(request.form['Price'])
            address = request.form['Address']
            pin_code = int(request.form['PinCode'])
            spots_count = int(request.form['SpotsCount'])
            new_lot = ParkingLot(name=name, price=price, address=address, pin_code=pin_code, spots_count=spots_count)
            db.session.add(new_lot)
            db.session.commit()
            for _ in range(spots_count):
                spot = ParkingSpot(lot_id=new_lot.id, status='A')
                db.session.add(spot)
            db.session.commit()
            return redirect(url_for('admin_routes.admin_dashboard'))
        return render_template('admin_add_parking_lot.html')
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if session.get('username') and session.get('role') == 'admin':
        admin = User.query.filter_by(username=session['username'], role='admin').first()
        if request.method == 'POST':
            admin.username = request.form['Username']
            admin.password = request.form['Password']
            db.session.commit()
            session['username'] = request.form['Username']
            return redirect(url_for('admin_routes.admin_dashboard'))
        return render_template('admin_edit_profile.html')
    return redirect(url_for('auth_routes.admin_login'))


@admin_routes.route('/admin-view-users')
def user_detail():
    if session.get('username') and session.get('role') == 'admin':
        users = User.query.filter_by(role='user').all()
        return render_template('admin_view_users.html', users=users)
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-view-user/<int:user_id>')
def view_user(user_id):
    if session.get('username') and session.get('role') == 'admin':
        user = User.query.get_or_404(user_id)
        reservations = ReserveParkingSpot.query.filter_by(user_id=user_id).all()
        return render_template('admin_view_user.html', user=user, reservations=reservations)
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-edit-parking-lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    if session.get('username') and session.get('role') == 'admin':
        lot = ParkingLot.query.get_or_404(lot_id)
        if request.method == 'POST':
            lot.name = request.form['LotName']
            lot.price = float(request.form['Price'])
            spots_count = int(request.form['SpotsCount'])
            active_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').order_by(ParkingSpot.id.desc()).all()
            active_count = len(active_spots)
            if spots_count < active_count:
                extra_count = active_count - spots_count
                surplus_spots = active_spots[:extra_count]
                for spot in surplus_spots:
                    if spot.status != 'A':
                        return render_template('error.html', message="Cannot reduce spots as some are currently occupied", retry_url=url_for('admin_routes.edit_lot', lot_id=lot_id))
                    spot.status = 'I'
            elif spots_count > active_count:
                add_count = spots_count - active_count
                reactivated = 0
                inactive_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='I').order_by(ParkingSpot.id.asc()).all()
                for spot in inactive_spots:
                    if reactivated < add_count:
                        spot.status = 'A'
                        reactivated += 1
                    else:
                        break
                for _ in range(add_count - reactivated):
                    db.session.add(ParkingSpot(lot_id=lot.id, status='A'))
            lot.spots_count = spots_count
            db.session.commit()
            return redirect(url_for('admin_routes.admin_dashboard'))
        can_delete_spot = (ParkingSpot.query.filter_by(lot_id=lot_id).filter(ParkingSpot.status == 'O').count() == 0)
        return render_template('admin_edit_parking_lot.html', lot=lot, can_delete_spot=can_delete_spot)
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-delete-parking-lot/<int:lot_id>', methods=['POST'])
def delete_parking_lot(lot_id):
    if session.get('username') and session.get('role') == 'admin':
        lot = ParkingLot.query.get_or_404(lot_id)
        active_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').all()
        for spot in active_spots:
            spot.status = 'I'
        db.session.commit()
        return redirect(url_for('admin_routes.admin_dashboard'))
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-view-parking-spot/<int:spot_id>', )
def view_parking_spot(spot_id):
    if session.get('username') and session.get('role') == 'admin':
        spot = ParkingSpot.query.get_or_404(spot_id)
        if not spot:
            return render_template('error.html', message="Parking Spot not found.", retry_url=url_for('admin_routes.admin_dashboard'))
        reservations = ReserveParkingSpot.query.filter_by(spot_id=spot_id).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
        return render_template('admin_view_parking_spot.html', spot=spot, reservations=reservations)
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-delete-parking-spot/<int:spot_id>', methods=['POST'])
def delete_parking_spot(spot_id):
    if session.get('username') and session.get('role') == 'admin':
        spot = ParkingSpot.query.get_or_404(spot_id)
        if spot.status != 'A':
            return render_template('error.html', message="Cannot deactivate the spot as it is not available.", retry_url=url_for('admin_routes.view_parking_spot', spot_id=spot_id))
        spot.status = 'I'
        db.session.commit()
        return redirect(url_for('admin_routes.admin_dashboard'))
    return redirect(url_for('auth_routes.admin_login'))

@admin_routes.route('/admin-activate-parking-spot/<int:spot_id>', methods=['POST'])
def activate_parking_spot(spot_id):
    if session.get('username') and session.get('role') == 'admin':
        spot = ParkingSpot.query.get_or_404(spot_id)
        if spot.status != 'I':
            return render_template('error.html', message="Cannot activate the available spot.", retry_url=url_for('admin_routes.view_parking_spot', spot_id=spot_id))
        spot.status = 'A'
        db.session.commit()
        return redirect(url_for('admin_routes.admin_dashboard'))
    return redirect(url_for('auth_routes.admin_login'))