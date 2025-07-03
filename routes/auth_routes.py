from flask import render_template, request, redirect, url_for, session, Blueprint
from models import db, User

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/user-registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        name = request.form['Name']
        age = int(request.form['Age'])
        username = request.form['Username']
        password = request.form['Password']
        if User.query.filter_by(username=username).first():
            return render_template('error.html', message="Username already taken.", retry_url=url_for('auth_routes.user_registration'))
        user = User(name=name, age=age, username=username, password=password, role='user')
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        session['role'] = 'user'
        return render_template('user_dashboard.html')
    return render_template('user_registration.html')

@auth_routes.route('/user-login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        if User.query.filter_by(username=username, password=password, role='user').first():
            session['username'] = username
            session['role'] = 'user'
            return redirect(url_for('user_routes.user_dashboard'))
        return render_template('error.html', message="Invalid user credentials.", retry_url=url_for('auth_routes.user_login'))
    return render_template('user_login.html')

@auth_routes.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        if User.query.filter_by(username=username, password=password, role='admin').first():
            session['username'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin_routes.admin_dashboard'))
        return render_template('error.html', message="Invalid admin credentials.", retry_url=url_for('auth_routes.admin_login'))
    return render_template('admin_login.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))