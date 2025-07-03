from flask import Flask, render_template
from models import db, User
from datetime import datetime
from routes.user_routes import user_routes
from routes.admin_routes import admin_routes
from routes.auth_routes import auth_routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "IITMProjectMay2025"
db.init_app(app)

app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(auth_routes)

def create_admin():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(name='admin', age=20, username='admin', password='admin', role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    date = datetime.now()
    return render_template('index.html', year=date.year, date=date.strftime("%d %B %Y"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()    
    app.run(debug=True) 