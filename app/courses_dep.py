from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_login import login_required, current_user
from flask.helpers import flash
from database import db
from utils import format_errors
from models import Course, Department, Role
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, InputRequired, Length

courses_dep = Blueprint("courses_dep", __name__)


def department_query():
    return Department.query.all()


class DepartmentsEditForm(FlaskForm):
    department1 = QuerySelectField('Department1 Courses',
                                   query_factory=department_query, allow_blank=True, get_label='name', render_kw={"class": "form-select"})
    department2 = QuerySelectField('Department2 Courses',
                                   query_factory=department_query, allow_blank=True, get_label='name', render_kw={"class": "form-select"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@courses_dep.route("", methods=["GET", "POST"])
@login_required
def view():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    return render_template('courses/dep_view.html',)


@courses_dep.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = DepartmentsEditForm(obj=current_user)

    if form.validate_on_submit():
        current_user.department1 = form.department1.data
        current_user.department2 = form.department2.data
        db.session.commit()
        flash("Departments have been saved!", "success")
        return render_template('courses/dep_view.html')
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('courses/dep_edit.html', form=form)
