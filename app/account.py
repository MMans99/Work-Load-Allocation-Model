from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length
from models import User
from database import db
from utils import format_errors

account = Blueprint("account", __name__)


class AccountEditForm(FlaskForm):
    university_id = StringField('University ID', validators=[
                                Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    fname = StringField('First Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    lname = StringField('Last Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    email = StringField('Email Address', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "pattern": "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


class AccountChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control", "autofocus": True})
    password_repeat = PasswordField('Repeat Password', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@account.route("")
@login_required
def view():
    return render_template("account/view.html")


@account.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = AccountEditForm(obj=current_user)

    if form.validate_on_submit():
        found_id = User.query.filter_by(
            university_id=form.university_id.data).first()
        found_id.fname = form.fname.data
        found_id.lname = form.lname.data
        found_id.email = form.email.data
        db.session.commit()
        flash("Account data has been saved!", "success")
        return redirect(url_for("account.view"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template("account/edit.html", form=form)


@account.route("/edit/password", methods=["GET", "POST"])
@login_required
def change_password():
    form = AccountChangePasswordForm(obj=current_user)
    if form.validate_on_submit():
        current_user.password = generate_password_hash(
            form.password.data, method='sha256')
        db.session.commit()
        flash("Account password has been saved!", "success")
        return redirect(url_for("account.view"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")
    return render_template('account/change_password.html', form=form)
