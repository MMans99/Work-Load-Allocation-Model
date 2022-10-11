from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired
from models import Role
from database import db
from utils import format_errors

allocation_r = Blueprint("allocation_r", __name__)


class AllocationRForm(FlaskForm):
    # Research
    r31 = FloatField('Teaching and Research Related Scholarship', validators=[InputRequired()], render_kw={
        "class": "form-control", "autofocus": True})
    r321 = FloatField('Journal Articles  (4 hours per paper per week)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    r322 = FloatField('Conference Articles  (2 hours per paper per week)',
                      validators=[InputRequired()], render_kw={"class": "form-control"})
    r33 = FloatField('New to University: Role Development',
                     validators=[InputRequired()], render_kw={"class": "form-control"})
    r34 = FloatField('Internally-Funded Research (2/1 hours per week per project for PI/Co-PI)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    r35 = FloatField('External Funded Research (3/1.5 hours per week per project for PI/Co-PI)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    r36 = FloatField('Support for research (2/1 hours per week per group for Coord./Member)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    r37 = FloatField('Patents', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    r38 = FloatField('Professional Development Activties--Research (0.25 hours per week)', validators=[
        InputRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Save', render_kw={
                         "class": "btn btn-primary"})


@allocation_r.route("")
@login_required
def view():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    sum = current_user.r31*40 + current_user.r321*4*40 + current_user.r322*2*40 + current_user.r33*40 + \
        current_user.r34*40 + current_user.r35*40 + current_user.r36 * \
        40 + current_user.r37*40 + current_user.r38*40
    return render_template("allocation/r_view.html", sum=sum)


@allocation_r.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if current_user.role == Role.ADMIN.value:
        return render_template("error/403_adv.html")

    form = AllocationRForm(obj=current_user)

    if form.validate_on_submit():
        current_user.r31 = form.r31.data
        current_user.r321 = form.r321.data
        current_user.r322 = form.r322.data
        current_user.r33 = form.r33.data
        current_user.r34 = form.r34.data
        current_user.r35 = form.r35.data
        current_user.r36 = form.r36.data
        current_user.r37 = form.r37.data
        current_user.r38 = form.r38.data
        db.session.commit()
        flash("Graduate Studies data has been saved!", "success")
        return redirect(url_for("allocation_r.view"))
    else:
        if form.errors:
            flash(format_errors(form.errors), "danger")

    return render_template("allocation/r_edit.html", form=form)
