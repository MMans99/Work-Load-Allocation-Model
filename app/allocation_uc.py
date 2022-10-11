from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired
from models import Role
from database import db
from utils import format_errors

allocation_uc = Blueprint("allocation_uc", __name__)


class AllocationUCForm(FlaskForm):
    # University and Community Service
    uc41 = FloatField('Accreditation and Related Administrative Tasks', validators=[InputRequired()], render_kw={
        "class": "form-control", "autofocus": True})
    uc42 = FloatField('Committee Work ', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    uc43 = FloatField('Teaching/Research Related Administration',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    uc44 = FloatField('Administrative Tasks/requests from Dept., College, University',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    uc45 = FloatField('Conference/Workshop Organization & Support', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    uc461 = FloatField('Editorial Board, Guest Editor ', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    uc462 = FloatField('Referee for Journals and Conferences', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    uc463 = FloatField('Membership in Professional Organizations', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    uc47 = FloatField('Consulting', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    uc48 = FloatField('Engagemwent in training and lifelong learning', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    uc49 = FloatField('Collaboration projects with the Community', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@allocation_uc.route("")
@login_required
def view():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    sum = current_user.uc41*40 + current_user.uc42*40 + current_user.uc43*40 + current_user.uc44*40 + current_user.uc45 * \
        40 + current_user.uc461*40 + current_user.uc462*40 + current_user.uc463 * \
        40 + current_user.uc47*40 + current_user.uc48*40 + current_user.uc49*40
    return render_template("allocation/uc_view.html", sum=sum)


@allocation_uc.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = AllocationUCForm(obj=current_user)

    if form.validate_on_submit():
        current_user.uc41 = form.uc41.data
        current_user.uc42 = form.uc42.data
        current_user.uc43 = form.uc43.data
        current_user.uc44 = form.uc44.data
        current_user.uc45 = form.uc45.data
        current_user.uc461 = form.uc461.data
        current_user.uc462 = form.uc462.data
        current_user.uc463 = form.uc463.data
        current_user.uc47 = form.uc47.data
        current_user.uc48 = form.uc48.data
        current_user.uc49 = form.uc49.data
        db.session.commit()
        flash("Graduate Studies data has been saved!", "success")
        return redirect(url_for("allocation_uc.view"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template("allocation/uc_edit.html", form=form)
