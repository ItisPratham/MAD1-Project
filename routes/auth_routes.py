from flask import render_template, request, redirect, url_for, Blueprint
from models import db, User
from flask_login import login_user, logout_user

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
        user = User(name=name, age=age, username=username, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('user_routes.user_dashboard'))
    return render_template('user_registration.html')

@auth_routes.route('/user-login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        user = User.query.filter_by(username=username, role='user').first()
        if  user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user_routes.user_dashboard'))
        return render_template('error.html', message="Invalid user credentials.", retry_url=url_for('auth_routes.user_login'))
    return render_template('user_login.html')

@auth_routes.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        admin = User.query.filter_by(username=username, role='admin').first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_routes.admin_dashboard'))
        return render_template('error.html', message="Invalid admin credentials.", retry_url=url_for('auth_routes.admin_login'))
    return render_template('admin_login.html')

@auth_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))