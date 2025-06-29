from flask import Flask, render_template, request, url_for, session, redirect
from models import db, User, ParkingLot, ParkingSpot, ReserveParkingSpot
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "IITMProjectMay2025"
db.init_app(app)

def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(name='admin', age=20, username='admin', password='admin', role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    date = datetime.now()
    return render_template('index.html', year=date.year, date=date.strftime("%d %B, %Y"))


@app.route('/user-registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        name = request.form['Name']
        age = int(request.form['Age'])
        username = request.form['Username']
        password = request.form['Password']
        if User.query.filter_by(username=username).first():
            return render_template('error.html', message="Username already taken.", retry_url=url_for('user_registration'))
        user = User(name=name, age=age, username=username, password=password, role='user')
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['role'] = 'user'
        return render_template('user_dashboard.html')
    return render_template('user_registration.html')

@app.route('/user-login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        if User.query.filter_by(username=username, password=password, role='user').first():
            session['username'] = username
            session['role'] = 'user'
            return redirect(url_for('user_dashboard'))
        return render_template('error.html', message="Invalid user credentials.", retry_url=url_for('user_login'))
    return render_template('user_login.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        if User.query.filter_by(username=username, password=password, role='admin').first():
            session['username'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        return render_template('error.html', message="Invalid admin credentials.", retry_url=url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/user-dashboard')
def user_dashboard():
    if session.get('username') and session.get('role') == 'user':
        return render_template('user_dashboard.html')
    return redirect(url_for('user_login'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if session.get('username') and session.get('role') == 'admin':
        return render_template('admin_dashboard.html')
    return redirect(url_for('admin_login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)