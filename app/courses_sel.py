from flask import Blueprint, redirect, url_for, render_template, request, session, jsonify
from flask_login import login_required, current_user
from flask.helpers import flash
from database import db
from utils import format_errors
from models import Course, Department, Role
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired, Length
from utils import selection_calc

courses_sel = Blueprint("courses_sel", __name__)


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class CoursesEditForm(FlaskForm):
    department1 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course1 = NonValidatingSelectField('Department Courses', coerce=int, validators=[], render_kw={
        "class": "form-select"})
    department2 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course2 = NonValidatingSelectField('Department Courses', coerce=int, validators=[InputRequired()], render_kw={
        "class": "form-select"})
    department3 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course3 = NonValidatingSelectField('Department Courses', coerce=int, validators=[InputRequired()], render_kw={
        "class": "form-select"})
    department4 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course4 = NonValidatingSelectField('Department Courses', coerce=int, validators=[InputRequired()], render_kw={
        "class": "form-select"})
    department5 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course5 = NonValidatingSelectField('Department Courses', coerce=int, validators=[InputRequired()], render_kw={
        "class": "form-select"})
    department6 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course6 = NonValidatingSelectField('Department Courses', coerce=int, validators=[InputRequired()], render_kw={
        "class": "form-select"})
    department7 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course7 = NonValidatingSelectField('Department Courses', coerce=int, validators=[InputRequired()], render_kw={
        "class": "form-select"})
    department8 = SelectField('User Departments', render_kw={
                              "class": "form-select"})
    course8 = NonValidatingSelectField('Department Courses', coerce=int, validators=[InputRequired()], render_kw={
        "class": "form-select"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@courses_sel.route("", methods=["GET", "POST"])
@login_required
def view():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    return render_template('courses/sel_view.html', total=selection_calc(current_user))


@courses_sel.route("/course/<department>")
@login_required
def course(department):
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    courses = Course.query.filter_by(department_id=department).all()
    courseArray = []

    for course in courses:
        courseObj = {}
        courseObj['id'] = course.id
        courseObj['name'] = course.name
        courseArray.append(courseObj)

    return jsonify({'courses': courseArray})


@courses_sel.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = CoursesEditForm()

    departments = []
    departments.append(current_user.department.id)
    if current_user.department1:
        departments.append(current_user.department1.id)
    if current_user.department2:
        departments.append(current_user.department2.id)
    departments = sorted(set(departments))
    choices = [(department, Department.query.filter_by(id=department).first().name)
               for department in departments]
    department = departments[0]

    form.department1.choices = choices
    form.department2.choices = choices
    form.department3.choices = choices
    form.department4.choices = choices
    form.department5.choices = choices
    form.department6.choices = choices
    form.department7.choices = choices
    form.department8.choices = choices

    if form.submit.data and form.validate_on_submit():
        if form.course1.data == 0:
            current_user.course1 = None
        else:
            current_user.course1_id = form.course1.data
        if form.course2.data == 0:
            current_user.course2 = None
        else:
            current_user.course2_id = form.course2.data
        if form.course3.data == 0:
            current_user.course3 = None
        else:
            current_user.course3_id = form.course3.data
        if form.course4.data == 0:
            current_user.course4 = None
        else:
            current_user.course4_id = form.course4.data
        if form.course5.data == 0:
            current_user.course5 = None
        else:
            current_user.course5_id = form.course5.data
        if form.course6.data == 0:
            current_user.course6 = None
        else:
            current_user.course6_id = form.course6.data
        if form.course7.data == 0:
            current_user.course7 = None
        else:
            current_user.course7_id = form.course7.data
        if form.course8.data == 0:
            current_user.course8 = None
        else:
            current_user.course8_id = form.course8.data
        db.session.commit()
        flash("Courses have been saved!", "success")
        return render_template('courses/sel_view.html', total=selection_calc(current_user))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('courses/sel_edit.html', form=form)
