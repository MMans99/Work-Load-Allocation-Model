from flask import Flask, render_template
from flask_login import LoginManager
import os
from database import db
from utils import load_data
from models import User
from anon import anon
from account import account
from dashboard import dashboard
from settings import settings
from user import user
from profile import profile
from rank import rank
from department import department
from course import course
from allocation_dt import allocation_dt
from allocation_gs import allocation_gs
from allocation_r import allocation_r
from allocation_uc import allocation_uc
from allocation_l import allocation_l
from allocation_summary import allocation_summary
from user_summary import user_summary
from courses_sel import courses_sel
from courses_dep import courses_dep
from department_summary import department_summary
from college_summary import college_summary

app = Flask(__name__, static_url_path='')

app.secret_key = os.urandom(24)
app.config.from_pyfile('config.cfg')

login_manager = LoginManager()
login_manager.login_view = 'anon.signin'
login_manager.init_app(app)

app.register_blueprint(anon, url_prefix='')
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.register_blueprint(settings, url_prefix='/settings')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(rank, url_prefix='/rank')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(department, url_prefix='/department')
app.register_blueprint(course, url_prefix='/course')
app.register_blueprint(allocation_dt, url_prefix='/allocation/dt')
app.register_blueprint(allocation_gs, url_prefix='/allocation/gs')
app.register_blueprint(allocation_r, url_prefix='/allocation/r')
app.register_blueprint(allocation_uc, url_prefix='/allocation/uc')
app.register_blueprint(allocation_l, url_prefix='/allocation/l')
app.register_blueprint(allocation_summary, url_prefix='/allocation/summary')
app.register_blueprint(user_summary, url_prefix='/user_summary')
app.register_blueprint(courses_sel, url_prefix='/courses_sel')
app.register_blueprint(courses_dep, url_prefix='/courses_dep')
app.register_blueprint(department_summary, url_prefix='/department_summary')
app.register_blueprint(college_summary, url_prefix='/college_summary')

db.init_app(app)
with app.app_context():
    # db.drop_all()
    db.create_all()
    # load_data(os.path.dirname(os.path.realpath(__file__)))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.errorhandler(404)
def not_found(e):
    return render_template("error/404.html")
