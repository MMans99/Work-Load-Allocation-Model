from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired
from models import Role
from database import db
from utils import format_errors
# HI
#

allocation_dt = Blueprint("allocation_dt", __name__)


class AllocationDTForm(FlaskForm):
    # Contact Hours (per week)
    dt111 = FloatField('Lectures', validators=[InputRequired()], render_kw={
        "class": "form-control", "autofocus": True})
    dt112 = FloatField('Laboratory (1.5 hour max per Lab course)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    dt113 = FloatField('SDP/FYP/Master Research Project Supervision',
                       validators=[InputRequired()], render_kw={"class": "form-control"})
    dt114 = FloatField('Direct Postgraduate Supervision (1 hour/student per week max 3 hours/week/ semester). (0.5 hour for co-supervision)',
                       validators=[InputRequired()], render_kw={"class": "form-control"})
    # Indirect Contact
    dt121 = FloatField('Scheduled drop ins/Office Hours (including advising)',
                       validators=[InputRequired()], render_kw={"class": "form-control"})
    dt122 = FloatField('Tutorials', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    dt123 = FloatField('Exam invigilation', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    dt124 = FloatField('Other', validators=[InputRequired()], render_kw={
        "class": "form-control"})
    dt13 = FloatField('Preparation (1 hour contact requires 1.5 preparation, assume 2 different courses)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    dt14 = FloatField('Preperation of Totally New Course (1 to 4 hours per course per week counted for 1 year)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    dt15 = FloatField('Assessment/Reassessment',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    dt16 = FloatField('Office Hour Courses/Practical Training (counted at 1/0.5 hours per student per week  for Office Course/Training)',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    dt17 = FloatField('Professional Development Activties--Teaching & Learning (0.25 hours per week)',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@allocation_dt.route("")
@login_required
def view():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    directteaching = current_user.dt111*32 + \
        current_user.dt112*32 + current_user.dt113*32 + current_user.dt114*32
    indirectteaching = current_user.dt121*32 + current_user.dt122*32 + current_user.dt123*32 + current_user.dt124 * \
        32 + current_user.dt13*32 + current_user.dt14*32 + \
        current_user.dt15*32 + current_user.dt16*32 + current_user.dt17*40
    sum = directteaching + indirectteaching
    return render_template("allocation/dt_view.html", sum=sum, directteaching=directteaching, indirectteaching=indirectteaching)


@allocation_dt.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = AllocationDTForm(obj=current_user)

    if form.validate_on_submit():
        current_user.dt111 = form.dt111.data
        current_user.dt112 = form.dt112.data
        current_user.dt113 = form.dt113.data
        current_user.dt114 = form.dt114.data
        current_user.dt121 = form.dt121.data
        current_user.dt122 = form.dt122.data
        current_user.dt123 = form.dt123.data
        current_user.dt124 = form.dt124.data
        current_user.dt13 = form.dt13.data
        current_user.dt14 = form.dt14.data
        current_user.dt15 = form.dt15.data
        current_user.dt16 = form.dt16.data
        current_user.dt17 = form.dt17.data
        db.session.commit()
        flash("Direct Teaching data has been saved!", "success")
        return redirect(url_for("allocation_dt.view"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template("allocation/dt_edit.html", form=form)
