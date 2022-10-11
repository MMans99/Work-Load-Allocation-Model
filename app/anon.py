from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from datetime import datetime, timedelta
import requests
import uuid
from database import db
from utils import format_errors
from models import User, Role, Rank, Profile, Department, Course
from mailgun import apikey, url

anon = Blueprint("anon", __name__)


class SigninForm(FlaskForm):
    university_id = StringField('', validators=[
                                Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "placeholder": "University ID", "autofocus": True})
    password = PasswordField('', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control", "placeholder": "Password"})
    submit = SubmitField('Sign In', render_kw={
                         "class": "w-100 btn btn-lg btn-primary"})


class ResetPasswordForm(FlaskForm):
    university_id = StringField('', validators=[
                                Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "placeholder": "University ID", "autofocus": True})
    submit = SubmitField('Reset', render_kw={
        "class": "w-100 btn btn-lg btn-primary"})


class SetPasswordForm(FlaskForm):
    password = PasswordField('', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control", "placeholder": "Password", "autofocus": True})
    password_repeat = PasswordField('', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control", "placeholder": "Repeat Password"})
    submit = SubmitField('Set Password', render_kw={
        "class": "w-100 btn btn-lg btn-primary"})


@anon.route("/")
@login_required
def home():
    if current_user.role == Role.ADMIN.value:
        return redirect(url_for('dashboard.view'))
    else:
        return redirect(url_for('account.view'))


@anon.route("/signin", methods=["GET", "POST"])
def signin():
    form = SigninForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            university_id=form.university_id.data).first()

        # check if the user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again.', 'danger')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('anon.signin'))
        else:
            login_user(user)
            return redirect(url_for('dashboard.view'))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('anon/signin.html', form=form)


@anon.route('/reset', methods=["GET", "POST"])
def reset():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        found_id = User.query.filter_by(
            university_id=form.university_id.data).first()
        if found_id:
            found_id.code = uuid.uuid4()
            found_id.code_date = datetime.utcnow()
            db.session.commit()
            requests.post(url, anon=("api", apikey),
                          data={"from": 'WLAM <postmaster@mg.sinjab.com>',
                                "to": [found_id.email],
                                "subject": "WLAM password reset",
                                "text": request.host_url + 'reset/' + form.university_id.data + '/' + found_id.code}
                          )
        flash("Reset link is sent to your email!", "info")
        return redirect(url_for("anon.signin"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('anon/password_reset.html', form=form)


@anon.route('/reset/<id>/<code>', methods=["GET", "POST"])
def reset_password(id, code):
    form = SetPasswordForm()

    if form.validate_on_submit():
        found_id = User.query.filter_by(university_id=id).first()
        if found_id:
            if found_id.code == code:
                if (found_id.password == ''):
                    found_id.code = ''
                    found_id.password = generate_password_hash(
                        request.form["password"], method='sha256')
                    db.session.commit()
                    flash("Password set successfully", "success")
                    return redirect(url_for("anon.signin"))
                else:
                    if (datetime.utcnow() - found_id.code_date) < timedelta(minutes=60):
                        found_id.code = ''
                        found_id.code_date = None
                        found_id.password = generate_password_hash(
                            request.form["password"], method='sha256')
                        db.session.commit()
                        flash("Password reset successfully", "success")
                        return redirect(url_for("anon.signin"))

        flash("Something went wrong!", "danger")
        return redirect(url_for("anon.signin"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('anon/password_set.html', id=id, code=code, form=form)


@anon.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('anon.home'))
