from flask import render_template, request, redirect, url_for, Blueprint
from models import db, User
from flask_login import login_user, logout_user
import re

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/user-registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        name = request.form['Name'].strip()
        age = int(request.form['Age'])
        username = request.form['Username'].strip().lower()
        password = request.form['Password']
        confirm_password = request.form.get('ConfirmPassword')

        if not re.match(r'^[A-Za-z\s]{3,}$', name):
            return render_template('error.html', message="Invalid name. Name must have atleast 3 characters.", retry_url=url_for('auth_routes.user_registration'))
        if not (18 <= age <= 99):
            return render_template('error.html', message="Invalid age. Age must be between 18 and 99.", retry_url=url_for('auth_routes.user_registration'))
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username):
            return render_template('error.html', message="Invalid email format.", retry_url=url_for('auth_routes.user_registration'))
        if password != confirm_password:
            return render_template('error.html', message="Passwords do not match.", retry_url=url_for('auth_routes.user_registration'))
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,12}$', password):
            return render_template('error.html', message="Password must be 8-12 characters long with atleast 1 num, and 1 uppercase and 1 lowercase alphabet.", retry_url=url_for('auth_routes.user_registration'))
        
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

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username):
            return render_template('error.html', message="Invalid email format.", retry_url=url_for('auth_routes.user_login'))
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,12}$', password):
            return render_template('error.html', message="Password must be 8-12 characters long with atleast 1 num, and 1 uppercase and 1 lowercase alphabet.", retry_url=url_for('auth_routes.user_login'))

        user = User.query.filter_by(username=username, role='user').first()
        if  user and user.check_password(password):
            login_user(user)
            return redirect(url_for('user_routes.user_dashboard'))
        return render_template('error.html', message="Invalid user credentials.", retry_url=url_for('auth_routes.user_login'))
    return render_template('user_login.html')

@auth_routes.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['Username'].strip().lower()
        password = request.form['Password']

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username):
            return render_template('error.html', message="Invalid email format.", retry_url=url_for('auth_routes.admin_login'))
        if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,12}$', password):
            return render_template('error.html', message="Password must be 8-12 characters long with atleast 1 num, and 1 uppercase and 1 lowercase alphabet.", retry_url=url_for('auth_routes.admin_login'))

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