from flask import Blueprint, redirect, url_for, render_template, request, session
from flask_login import login_required, current_user
from flask.helpers import flash
from database import db
from utils import format_errors
from models import Profile, Role
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, InputRequired, Length

profile = Blueprint("profile", __name__)


class ProfileCreateForm(FlaskForm):
    name = StringField('Name', validators=[
        Required(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    direct_teaching = IntegerField('Direct Teaching', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    direct_teaching_percent = IntegerField('Direct Teaching Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    direct_teaching_minimum = IntegerField('Direct Teaching Minimum', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    supervision = IntegerField('Supervision', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    supervision_percent = IntegerField('Supervision Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    research = IntegerField('Research', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    research_percent = IntegerField('Research Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    university_service = IntegerField('University Service', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    university_service_percent = IntegerField('University Service Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    lead_manage_admin = IntegerField('Lead Manage Admin', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    lead_manage_admin_percent = IntegerField('Lead Manage Admin Percent"', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Create', render_kw={
                         "class": "btn btn-primary"})


class ProfileEditForm(FlaskForm):
    name = StringField('Name', validators=[
        InputRequired(), Length(min=3, max=50)], render_kw={"class": "form-control", "autofocus": True})
    direct_teaching = IntegerField('Direct Teaching', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    direct_teaching_percent = IntegerField('Direct Teaching Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    direct_teaching_minimum = IntegerField('Direct Teaching Minimum', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    supervision = IntegerField('Supervision', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    supervision_percent = IntegerField('Supervision Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    research = IntegerField('Research', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    research_percent = IntegerField('Research Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    university_service = IntegerField('University Service', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    university_service_percent = IntegerField('University Service Percent', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    lead_manage_admin = IntegerField('Lead Manage Admin', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    lead_manage_admin_percent = IntegerField('Lead Manage Admin Percent"', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


class ProfileDeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={
                         "class": "btn btn-primary"})


@profile.route("")
@login_required
def list():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    return render_template("profile/list.html", profiles=Profile.query.all())


@profile.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = ProfileCreateForm()

    if form.validate_on_submit():
        prfl = Profile(name=form.name.data, direct_teaching=form.direct_teaching.data, direct_teaching_percent=form.direct_teaching_percent.data, direct_teaching_minimum=form.direct_teaching_minimum.data, supervision=form.supervision.data, supervision_percent=form.supervision_percent.data,
                       research=form.research.data, research_percent=form.research_percent.data, university_service=form.university_service.data, university_service_percent=form.university_service_percent.data, lead_manage_admin=form.lead_manage_admin.data, lead_manage_admin_percent=form.lead_manage_admin_percent.data)
        db.session.add(prfl)
        db.session.commit()
        flash("Profile has been created!", "success")
        return redirect(url_for("profile.view", id=prfl.id))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template('profile/create.html', form=form)


@profile.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_profile = Profile.query.filter_by(id=id).first()
    if found_profile:
        form = ProfileEditForm(obj=found_profile)
        if form.validate_on_submit():
            found_profile.name = form.name.data
            found_profile.direct_teaching = form.direct_teaching.data
            found_profile.direct_teaching_percent = form.direct_teaching_percent.data
            found_profile.direct_teaching_minimum = form.direct_teaching_minimum.data
            found_profile.supervision = form.supervision.data
            found_profile.supervision_percent = form.supervision_percent.data
            found_profile.research = form.research.data
            found_profile.research_percent = form.research_percent.data
            found_profile.university_service = form.university_service.data
            found_profile.university_service_percent = form.university_service_percent.data
            found_profile.lead_manage_admin = form.lead_manage_admin.data
            found_profile.lead_manage_admin_percent = form.lead_manage_admin_percent.data
            db.session.commit()
            flash("Profile has been edited!", "success")
            return redirect(url_for("profile.view", id=found_profile.id))
        else:
            if form.errors:
                flash(format_errors(form.errors), "danger")
        return render_template('profile/edit.html', found_profile=found_profile, form=form)
    else:
        return render_template("error/404_adv.html")


@profile.route("/delete/<id>", methods=["GET", "POST"])
@login_required
def delete(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_profile = Profile.query.filter_by(id=id).first()
    if found_profile:
        form = ProfileDeleteForm()
        if form.validate_on_submit():
            db.session.delete(found_profile)
            db.session.commit()
            flash("Profile has been deleted!", "success")
            return redirect(url_for("profile.list"))
        return render_template('profile/delete.html', found_profile=found_profile, form=form)
    else:
        return render_template("error/404_adv.html")


@profile.route("/<id>")
@login_required
def view(id):
    if current_user.role != Role.ADMIN.value:
        return render_template("error/403_adv.html")

    found_profile = Profile.query.filter_by(id=id).first()
    if found_profile:
        return render_template("profile/view.html", found_profile=found_profile)
    else:
        return render_template("error/404_adv.html")
