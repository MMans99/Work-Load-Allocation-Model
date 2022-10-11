from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Role, User
from database import db
from utils import format_errors
from sqlalchemy.sql import func

college_summary = Blueprint("college_summary", __name__)


@college_summary.route("")
@login_required
def view():
    if current_user.role < Role.VICEDEAN.value:
        return render_template("error/403_adv.html")

    qry = db.session.query(func.avg(User.dt111).label("average_week")).one()
    average_week = qry.average_week
    average_sem = float(average_week) * 16
    average_indirect = float(average_sem) * 2.5
    average_total = float(average_sem) + float(average_indirect)

    return render_template("summary/college.html", average_week=round(average_week, 1), average_sem=round(average_sem, 1), average_indirect=round(average_indirect, 1), average_total=round(average_total, 1))
