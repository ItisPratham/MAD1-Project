from flask import render_template, redirect, url_for, session, Blueprint

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user-dashboard')
def user_dashboard():
    if session.get('username') and session.get('role') == 'user':
        return render_template('user_dashboard.html')
    return redirect(url_for('auth_routes.user_login'))