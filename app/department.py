from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_login import login_required, current_user
from flask.helpers import flash
from database import db
from utils import format_errors
from models import Department, Role
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length

department = Blueprint("department", __name__)


class DepartmentCreateForm(FlaskForm):
    university_id = StringField('University ID', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    name = StringField('Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    submit = SubmitField('Create', render_kw={
                         "class": "btn btn-primary"})


class DepartmentEditForm(FlaskForm):
    university_id = StringField('University ID', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    name = StringField('Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


class DepartmentDeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={
                         "class": "btn btn-primary"})


@department.route("")
@login_required
def list():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    return render_template("department/list.html", departments=Department.query.all())


@department.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = DepartmentCreateForm()

    if form.validate_on_submit():
        rnk = Department(form.university_id.data, form.name.data)
        db.session.add(rnk)
        db.session.commit()
        flash("Department has been created!", "success")
        return redirect(url_for("department.view", id=rnk.id))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('department/create.html', form=form)


@department.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_department = Department.query.filter_by(id=id).first()
    if found_department:
        form = DepartmentEditForm(obj=found_department)
        if form.validate_on_submit():
            found_department.university_id = form.university_id.data
            found_department.name = form.name.data
            db.session.commit()
            flash("Department has been edited!", "success")
            return redirect(url_for("department.view", id=found_department.id))
        else:
            if form.errors:
                flash(format_errors(form.errors), "danger")
        return render_template('department/edit.html', found_department=found_department, form=form)
    else:
        return render_template("error/404_adv.html")


@department.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_department = Department.query.filter_by(id=id).first()
    if found_department:
        form = DepartmentDeleteForm()
        if form.validate_on_submit():
            db.session.delete(found_department)
            db.session.commit()
            flash("Department has been deleted!", "success")
            return redirect(url_for("department.list"))
        return render_template('department/delete.html', found_department=found_department, form=form)
    else:
        return render_template("error/404_adv.html")


@department.route("/<id>")
@login_required
def view(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_department = Department.query.filter_by(id=id).first()
    if found_department:
        return render_template("department/view.html", found_department=found_department)
    else:
        return render_template("error/404_adv.html")
