from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Role, User, Department
from database import db
from utils import format_errors
from sqlalchemy.sql import func

department_summary = Blueprint("department_summary", __name__)


@department_summary.route("/list")
@login_required
def list():
    if current_user.role < Role.VICEDEAN.value:
        return render_template("error/403_adv.html")

    departments = Department.query.all()
    arr = []
    for department in departments:
        count = db.session.query(User.id).filter_by(
            department_id=department.id).count()
        arr.append((department, count))

    return render_template("summary/departments.html", arr=arr)


@department_summary.route("")
@login_required
def view():
    if current_user.role > Role.CHAIRMAN.value:
        return render_template("error/403_adv.html")

    qry = db.session.query(func.avg(User.dt111).label(
        "average_week")).filter_by(department_id=current_user.department_id).one()
    average_week = qry.average_week if qry.average_week else 0
    average_sem = float(average_week) * 16
    average_indirect = float(average_sem) * 2.5
    average_total = float(average_sem) + float(average_indirect)

    return render_template("summary/department.html", department_name=current_user.department.name, average_week=round(average_week, 1), average_sem=round(average_sem, 1), average_indirect=round(average_indirect, 1), average_total=round(average_total, 1))


@department_summary.route("/<department_id>")
@login_required
def view_id(department_id):
    if current_user.role < Role.VICEDEAN.value:
        return render_template("error/403_adv.html")

    qry = db.session.query(func.avg(User.dt111).label(
        "average_week")).filter_by(department_id=department_id).one()
    average_week = qry.average_week if qry.average_week else 0
    average_sem = float(average_week) * 16
    average_indirect = float(average_sem) * 2.5
    average_total = float(average_sem) + float(average_indirect)

    return render_template("summary/department.html", department_name=Department.query.filter_by(id=department_id).one().name, average_week=round(average_week, 1), average_sem=round(average_sem, 1), average_indirect=round(average_indirect, 1), average_total=round(average_total, 1))
