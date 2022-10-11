from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_login import login_required, current_user
from flask.helpers import flash
from database import db
from utils import format_errors
from models import Course, Department, Role, CourseType
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, InputRequired, Length

course = Blueprint("course", __name__)


def department_query():
    return Department.query


class CourseCreateForm(FlaskForm):
    university_id = StringField('University ID', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    name = StringField('Name', validators=[Required(), Length(
        min=3, max=50)], render_kw={"class": "form-control"})
    credit = FloatField('Credit', validators=[InputRequired()], render_kw={
        "class": "form-control"})
    department = QuerySelectField(query_factory=department_query, allow_blank=False,
                                  get_label='name', render_kw={"class": "form-select"})
    course_type = SelectField(
        'Course Type', choices=[(CourseType.NORMAL.value, 'Normal Course'), (CourseType.LAB.value, 'Laboratory'), (CourseType.EMBEDDED.value, 'Embedded Course'), (CourseType.MASTER.value, 'Master Course'), (CourseType.PHD.value, 'Phd Course')], render_kw={"class": "form-select"})
    submit = SubmitField('Create', render_kw={
                         "class": "btn btn-primary"})


class CourseEditForm(FlaskForm):
    university_id = StringField('University ID', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    name = StringField('Name', validators=[Required(), Length(
        min=3, max=50)], render_kw={"class": "form-control"})
    credit = FloatField('Credit', validators=[InputRequired()], render_kw={
        "class": "form-control"})
    department = QuerySelectField(query_factory=department_query, allow_blank=False,
                                  get_label='name', render_kw={"class": "form-select"})
    course_type = SelectField(
        'Course Type', choices=[(CourseType.NORMAL.value, 'Normal Course'), (CourseType.LAB.value, 'Laboratory'), (CourseType.EMBEDDED.value, 'Embedded Course'), (CourseType.MASTER.value, 'Master Course'), (CourseType.PHD.value, 'Phd Course')], render_kw={"class": "form-select"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


class CourseDeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={
                         "class": "btn btn-primary"})


@course.route("")
@login_required
def list():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    courses = Course.query.all()
    arr = []
    for course in courses:
        if course.course_type == CourseType.NORMAL.value:
            effort = course.credit
        if course.course_type == CourseType.MASTER.value:
            effort = course.credit*1.2
        if course.course_type == CourseType.PHD.value:
            effort = course.credit*1.5
        if course.course_type == CourseType.EMBEDDED.value:
            effort = course.credit + 0.5
        if course.course_type == CourseType.LAB.value:
            effort = course.credit * 1.5
        arr.append((course, round(effort, 1)))

    return render_template("course/list.html", courses=Course.query.all(), arr=arr)


@course.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = CourseCreateForm()

    if form.validate_on_submit():
        crs = Course(university_id=form.university_id.data, name=form.name.data,
                     credit=form.credit.data, course_type=form.course_type.data, department_id=form.department.data.id)
        db.session.add(crs)
        db.session.commit()
        flash("Course has been created!", "success")
        return redirect(url_for("course.view", id=crs.id))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('course/create.html', form=form)


@course.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_course = Course.query.filter_by(id=id).first()
    if found_course:
        form = CourseEditForm(obj=found_course)
        if form.validate_on_submit():
            found_course.university_id = form.university_id.data
            found_course.name = form.name.data
            found_course.credit = form.credit.data
            found_course.course_type = form.course_type.data
            found_course.department = form.department.data
            db.session.commit()
            flash("Course has been edited!", "success")
            return redirect(url_for("course.view", id=found_course.id))
        else:
            if form.errors:
                flash(format_errors(form.errors), "danger")
        return render_template('course/edit.html', found_course=found_course, form=form)
    else:
        return render_template("error/404_adv.html")


@course.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_course = Course.query.filter_by(id=id).first()
    if found_course:
        form = CourseDeleteForm()
        if form.validate_on_submit():
            db.session.delete(found_course)
            db.session.commit()
            flash("Course has been deleted!", "success")
            return redirect(url_for("course.list"))
        return render_template('course/delete.html', found_course=found_course, form=form)
    else:
        return render_template("error/404_adv.html")


@course.route("/<id>")
@login_required
def view(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_course = Course.query.filter_by(id=id).first()
    if found_course:
        if found_course.course_type == CourseType.NORMAL.value:
            effort = found_course.credit
        if found_course.course_type == CourseType.LAB.value:
            effort = found_course.credit*1.5
        if found_course.course_type == CourseType.MASTER.value:
            effort = found_course.credit*1.2
        if found_course.course_type == CourseType.PHD.value:
            effort = found_course.credit*1.5
        if found_course.course_type == CourseType.EMBEDDED.value:
            effort = found_course.credit + 0.5
        return render_template("course/view.html", found_course=found_course, effort=round(effort, 1))
    else:
        return render_template("error/404_adv.html")
