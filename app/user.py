from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from flask.helpers import flash
from database import db
from utils import format_errors
from models import User, Role, Rank, Profile, Department
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length
from werkzeug.security import generate_password_hash
import requests
import uuid
from mailgun import apikey, url

user = Blueprint("user", __name__)


def rank_query():
    return Rank.query


def department_query():
    return Department.query


def profile_query():
    return Profile.query


class UserCreateForm(FlaskForm):
    university_id = StringField('University ID', validators=[
                                Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    fname = StringField('First Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    lname = StringField('Last Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    email = StringField('Email Address', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "pattern": "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"})
    rank = QuerySelectField(query_factory=rank_query, allow_blank=False,
                            get_label='name', get_pk=lambda x: x.id, render_kw={"class": "form-select"})
    department = QuerySelectField(query_factory=department_query, allow_blank=False,
                                  get_label='name', render_kw={"class": "form-select"})
    department1 = QuerySelectField(query_factory=department_query, allow_blank=False,
                                   get_label='name', render_kw={"class": "form-select"})
    department2 = QuerySelectField(query_factory=department_query, allow_blank=False,
                                   get_label='name', render_kw={"class": "form-select"})
    profile = QuerySelectField(query_factory=profile_query, allow_blank=False,
                               get_label='name', render_kw={"class": "form-select"})
    role = SelectField(
        'Role', choices=[(Role.USER.value, 'Normal User'), (Role.CHAIRMAN.value, 'Chairman'), (Role.VICEDEAN.value, 'Vice Dean Assistant Dean'), (Role.DEAN.value, 'Dean'), (Role.ADMIN.value, 'Administrator')], render_kw={"class": "form-select"})
    submit = SubmitField('Create', render_kw={
                         "class": "btn btn-primary"})


class UserEditForm(FlaskForm):
    university_id = StringField('University ID', validators=[
                                Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    fname = StringField('First Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    lname = StringField('Last Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    email = StringField('Email Address', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "pattern": "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"})
    rank = QuerySelectField(query_factory=rank_query, allow_blank=False,
                            get_label='name', render_kw={"class": "form-select"})
    department = QuerySelectField(query_factory=department_query, allow_blank=False,
                                  get_label='name', render_kw={"class": "form-select"})
    department1 = QuerySelectField(query_factory=department_query, allow_blank=False,
                                   get_label='name', render_kw={"class": "form-select"})
    department2 = QuerySelectField(query_factory=department_query, allow_blank=False,
                                   get_label='name', render_kw={"class": "form-select"})
    profile = QuerySelectField(query_factory=profile_query, allow_blank=False,
                               get_label='name', render_kw={"class": "form-select"})
    role = SelectField(
        'Role', choices=[(Role.USER.value, 'Normal User'), (Role.CHAIRMAN.value, 'Chairman'), (Role.VICEDEAN.value, 'Vice Dean \ Assistant Dean'), (Role.DEAN.value, 'Dean'), (Role.ADMIN.value, 'Administrator')], render_kw={"class": "form-select"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


class UserChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control", "autofocus": True})
    password_repeat = PasswordField('Repeat Password', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


class UserDeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={
                         "class": "btn btn-primary"})


@user.route("")
@login_required
def list():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    return render_template("user/list.html", users=User.query.order_by("university_id").all())


@user.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = UserCreateForm()

    if form.validate_on_submit():
        found_user = User.query.filter_by(
            university_id=form.university_id.data).first()
        if found_user:
            flash("User id already exists!", "danger")
            return redirect(url_for("user/create"))
        else:
            usr = User(university_id=form.university_id.data, fname=form.fname.data, lname=form.lname.data, email=form.email.data, password='', role=form.role.data, rank_id=form.rank.data.id,
                       profile_id=form.profile.data.id, department_id=form.department.data.id, department1_id=form.department1.data.id, department2_id=form.department2.data.id)
            db.session.add(usr)
            usr.code = uuid.uuid4()
            db.session.commit()
            requests.post(url, auth=("api", apikey),
                          data={"from": 'WLAM <postmaster@mg.sinjab.com>',
                                "to": [usr.email],
                                "subject": "WLAM email confirm",
                                "text": request.host_url + 'reset/' + form.university_id.data + '/' + usr.code}
                          )
            flash("User has been created!", "success")
            return redirect(url_for("user.view", id=usr.id))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('user/create.html', form=form)


@user.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_user = User.query.filter_by(id=id).first()
    if found_user:
        form = UserEditForm(obj=found_user)
        if form.validate_on_submit():
            found_user.university_id = form.university_id.data
            found_user.fname = form.fname.data
            found_user.lname = form.lname.data
            found_user.email = form.email.data
            found_user.role = form.role.data
            found_user.rank = form.rank.data
            found_user.profile = form.profile.data
            found_user.department = form.department.data
            found_user.department1 = form.department1.data
            found_user.department2 = form.department2.data
            db.session.commit()
            flash("User has been edited!", "success")
            return redirect(url_for("user.view", id=found_user.id))
        else:
            if form.errors:
                flash(format_errors(form.errors), "danger")
        return render_template('user/edit.html', found_user=found_user, form=form)
    else:
        return render_template("error/404_adv.html")


@user.route("/edit/password/<id>", methods=["GET", "POST"])
@login_required
def change_password(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_user = User.query.filter_by(id=id).first()
    if found_user:
        form = UserChangePasswordForm(obj=found_user)
        if form.validate_on_submit():
            found_user.password = generate_password_hash(
                form.password.data, method='sha256')
            db.session.commit()
            flash("User password has been saved!", "success")
            return redirect(url_for("user.view", id=found_user.id))
        else:
            if form.errors:
                flash(format_errors(form.errors), "danger")
        return render_template('user/change_password.html', found_user=found_user, form=form)
    else:
        return render_template("error/404_adv.html")


@user.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_user = User.query.filter_by(id=id).first()
    if found_user:
        form = UserDeleteForm()
        if form.validate_on_submit():
            db.session.delete(found_user)
            db.session.commit()
            flash("User has been deleted!", "success")
            return redirect(url_for("user.list"))
        return render_template('user/delete.html', found_user=found_user, form=form)
    else:
        return render_template("error/404_adv.html")


@user.route("/<id>")
@login_required
def view(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_user = User.query.filter_by(id=id).first()
    if found_user:
        return render_template("user/view.html", found_user=found_user)
    else:
        return render_template("error/404_adv.html")
