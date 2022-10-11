from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length
from models import Role
from database import db

settings = Blueprint("settings", __name__)


class ProfileForm(FlaskForm):
    university_id = StringField('University ID', validators=[
                                Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    fname = StringField('First Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    lname = StringField('Last Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control"})
    email = StringField('Email Address', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "pattern": "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"})
    password = PasswordField('Password', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control"})
    password_repeat = PasswordField('Repeat Password', validators=[
        Required(), Length(min=8, max=30)], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@settings.route("/")
@login_required
def view():
    return render_template("settings/settings.html")
